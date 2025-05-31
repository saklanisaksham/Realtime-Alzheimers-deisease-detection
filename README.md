![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-green)


# Realtime-Alzheimers-deisease-detection
👁️ Blink Detection, Gaze Tracking & Speech Recognition App

This project is a Streamlit-based interactive application that uses computer vision and speech recognition techniques to:
- Detect **blinks** and **track pupil size**
- Perform **gaze movement analysis**
- Assess **speech accuracy** from a given paragraph
  
#🚀 Features

🔹 Blink Detection & Pupil Tracking
-- Uses Eye Aspect Ratio (EAR) to detect blinks.
-- Tracks left and right iris radius in real-time.
-- Blinks are counted and analyzed over a 60-second session.
-- Option to capture frame snapshots.
-- Displays warning if blinks exceed a threshold—potential Alzheimer's indicator.

🔹 Gaze Tracking
-- Monitors eye movement across the screen.
-- Calculates variation in gaze direction using facial landmarks.
-- Quantifies focus and attention level.

🔹 Speech Recognition
-- Displays a reference paragraph for the user to read.
-- Records and transcribes speech using Google Speech API.
-- Compares transcribed speech with reference text.
-- Calculates speech match accuracy percentage.

### 🛠️ Tech Stack

| Library              | Purpose                                |
|----------------------|----------------------------------------|
| **OpenCV**           | Video frame processing                 |
| **MediaPipe**        | Facial landmark and iris detection     |
| **Streamlit**        | Interactive Web UI                     |
| **SpeechRecognition**| Voice-to-text conversion               |
| **NumPy**, **SciPy** | Numerical computation                  |
| **Threading**        | Real-time processing optimization      |



### 📦 Installation

Follow these steps to set up and run the project locally:

```bash
# Clone the repository
git clone https://github.com/saklanisaksham/Realtime-Alzheimers-deisease-detection.git

# Navigate to the project directory
cd Realtime-Alzheimers-deisease-detection

# Install required dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run <filename>.py  # Replace <filename>.py with your actual script name

```

📸 Blink Detection Module Demo

- Press "Capture Image" to take a snapshot of the current webcam feed.
- Press "Reset Blink Count" to start blink counting again.
- After 60 seconds, results will display whether blink frequency is within a healthy range.

🧠 Cognitive Tests

Gaze Tracking: 
- Click "Start Gaze Test" to track eye movement for 60 seconds.
- Speech Recognition: Read the given paragraph aloud and press "Start Speech Test".
- Results will show spoken text and match accuracy with the original paragraph. 

### 📈 Result Interpretation

| Test Component   | Indicator                                         |
|------------------|---------------------------------------------------|
| **Blink Rate**   | >20 blinks → ⚠️ Possible Alzheimer sign           |
| **Pupil Size**   | Displayed in mm for analysis                      |
| **Gaze Variation**| Higher = poor focus (possible attention issues)  |
| **Speech Accuracy**| Lower % = possible speech or memory difficulty  |
