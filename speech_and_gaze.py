import cv2
import numpy as np
import mediapipe as mp
import streamlit as st
import time
import speech_recognition as sr
from difflib import SequenceMatcher

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Constants
TEXT_TO_READ = "This is the sample paragraph for gaze tracking and speech recognition. Please read it aloud."
DURATION = 60  # in seconds

def calculate_gaze_movement(landmarks, img_w, img_h):
    """Calculate rough gaze movement based on eye positions."""
    left_eye = [landmarks[i] for i in [33, 160, 158, 133, 153, 144]]
    right_eye = [landmarks[i] for i in [362, 385, 387, 263, 373, 380]]
    eye_center_x = np.mean([p[0] for p in left_eye + right_eye])
    return eye_center_x / img_w  # Normalize movement

def start_gaze_tracking():
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    gaze_movements = []
    frame_placeholder = st.empty()

    while time.time() - start_time < DURATION:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access the camera.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            landmarks = np.array([[p.x * img_w, p.y * img_h] for p in results.multi_face_landmarks[0].landmark])
            gaze_movements.append(calculate_gaze_movement(landmarks, img_w, img_h))

        frame_placeholder.image(frame, channels="BGR")

    cap.release()
    return np.std(gaze_movements) if gaze_movements else 0

def start_speech_recognition():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        st.info("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        spoken_text = recognizer.recognize_google(audio)
        return spoken_text
    except sr.UnknownValueError:
        return "(Speech not recognized)"
    except sr.RequestError:
        return "(Speech service unavailable)"

def compare_text(original, spoken):
    return SequenceMatcher(None, original, spoken).ratio() * 100

# Streamlit UI
st.title("Eye Movement and Speech Accuracy Test")

test_choice = st.radio("Choose a test:", ("Gaze Tracking", "Speech Recognition"))

if test_choice == "Gaze Tracking":
    st.markdown("### Follow the on-screen text with your eyes.")
    if st.button("Start Gaze Test"):
        gaze_variation = start_gaze_tracking()
        st.markdown(f"**Gaze Movement Variation:** {gaze_variation:.4f} (higher = more movement)")

elif test_choice == "Speech Recognition":
    st.markdown("### Read the text below aloud:")
    st.markdown(f"<h2 style='text-align: center;'>{TEXT_TO_READ}</h2>", unsafe_allow_html=True)
    if st.button("Start Speech Test"):
        spoken_text = start_speech_recognition()
        match_percentage = compare_text(TEXT_TO_READ, spoken_text)
        
        st.markdown("### Test Results")
        st.markdown(f"**Spoken Text:** {spoken_text}")
        st.markdown(f"**Match Accuracy:** {match_percentage:.2f}%")