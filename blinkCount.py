import cv2 as cv
import numpy as np
import mediapipe as mp
import streamlit as st
import threading
from scipy.spatial import distance as dist
import datetime
import os
import time

# Streamlit UI
st.title("Blink Detection and Pupil Tracking")
frame_placeholder = st.empty()
blink_placeholder = st.empty()

# Button for capturing image
capture_button = st.button("Capture Image")
reset_button = st.button("Reset Blink Count")

# Initialize Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
)

# Eye landmarks
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

# Constants
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 3
calibration_factor = 0.1
DURATION = 60  # Run for 60 seconds

# Shared Variables
blink_counter = 0
total_blinks = 0
latest_frame = None
stop_flag = False

def calculate_ear(eye_points, landmarks):
    """Calculate Eye Aspect Ratio (EAR) for blink detection."""
    vertical1 = dist.euclidean(landmarks[eye_points[1]], landmarks[eye_points[5]])
    vertical2 = dist.euclidean(landmarks[eye_points[2]], landmarks[eye_points[4]])
    horizontal = dist.euclidean(landmarks[eye_points[0]], landmarks[eye_points[3]])
    return (vertical1 + vertical2) / (2.0 * horizontal)

def capture_image(frame, directory="image_captured"):
    """Capture and save an image."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = os.path.join(directory, f"{timestamp}.jpg")
    cv.imwrite(filepath, frame)
    st.success(f"✅ Image saved to: {filepath}")

def video_processing():
    """Handles webcam feed, blink detection, and pupil tracking in a separate thread."""
    global blink_counter, total_blinks, latest_frame, stop_flag

    cap = cv.VideoCapture(0)
    start_time = time.time()  # Start timer

    while time.time() - start_time < DURATION:
        ret, frame = cap.read()
        if not ret:
            st.error("🚨 Failed to access the webcam")
            break

        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            mesh_points = np.array([
                np.multiply([p.x, p.y], [img_w, img_h]).astype(int)
                for p in results.multi_face_landmarks[0].landmark
            ])

            # Blink Detection
            left_ear = calculate_ear(LEFT_EYE, mesh_points)
            right_ear = calculate_ear(RIGHT_EYE, mesh_points)
            ear = (left_ear + right_ear) / 2.0

            if ear < EAR_THRESHOLD:
                blink_counter += 1
            else:
                if blink_counter >= CONSEC_FRAMES:
                    total_blinks += 1
                blink_counter = 0

            # Draw Blink Count
            cv.putText(frame, f"Blinks: {total_blinks}", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Iris Detection
            (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            cv.circle(frame, (int(l_cx), int(l_cy)), int(l_radius), (0, 255, 0), 2)
            cv.circle(frame, (int(r_cx), int(r_cy)), int(r_radius), (0, 255, 0), 2)

            # Convert radius to millimeters
            l_radius_mm = l_radius * calibration_factor
            r_radius_mm = r_radius * calibration_factor

            # Display pupil size
            cv.putText(frame, f"Left Pupil: {l_radius_mm:.2f} mm", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv.putText(frame, f"Right Pupil: {r_radius_mm:.2f} mm", (10, 120), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        latest_frame = frame.copy()
        time.sleep(0.03)  # Reduce CPU usage (smooth UI updates)

    cap.release()
    cv.destroyAllWindows()

# Start webcam thread
thread = threading.Thread(target=video_processing, daemon=True)
thread.start()

# Streamlit UI Loop
start_time = time.time()  # Start time tracking
while time.time() - start_time < DURATION:
    if latest_frame is not None:
        frame_placeholder.image(latest_frame, channels="BGR")

    blink_placeholder.write(f"**Total Blinks: {total_blinks}**")

    if capture_button:
        if latest_frame is not None:
            capture_image(latest_frame)
        capture_button = False  # Prevent multiple captures

    if reset_button:
        total_blinks = 0
        blink_counter = 0
        blink_placeholder.write("**Total Blinks: 0**")

    time.sleep(0.1)  # Prevents Streamlit UI from freezing

# **Final Analysis**
if total_blinks > 20:
    st.error("⚠️ **Signs of Alzheimer's detected!** Blinks exceeded normal range.")
else:
    st.success("✅ No abnormal blinking detected. No detection of Alzheimer")