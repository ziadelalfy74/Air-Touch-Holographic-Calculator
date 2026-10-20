# 🚀 Air-Touch Holographic Calculator

A futuristic, touchless Python-based calculator powered by **Computer Vision**, **MediaPipe**, and **OpenCV**. This application allows users to interact with a virtual holographic keypad in mid-air using precise hand-tracking and a **Thumb-Index Pinch (Pinch-to-Click)** mechanic.

---

## ✨ Features
- **Touchless Air-Interaction**: Control the calculator entirely in mid-air using your hand.
- **Precise Pinch Mechanics**: Utilizes a strict Thumb & Index finger pinch-and-release state machine to prevent accidental multiple inputs or spamming.
- **Real-time Skeleton Tracking**: Cyber-glove style visual hand tracking via Google's MediaPipe Tasks (`IMAGE` running mode for zero latency).
- **Holographic UI Design**: Aesthetic translucent button grid with dynamic hover highlighting (yellow) and active click feedback (green).
- **Smart Decimal Formatting**: Automatically formats calculation results to a maximum of 4 decimal places to keep the digital screen clean and organized.
- **Auditory Feedback**: Integrated Windows beep sounds on successful button clicks.

---

## 🛠️ Tech Stack
- **Python**
- **OpenCV** (Image processing & UI rendering)
- **MediaPipe Tasks Vision** (Gesture & Landmark Recognition)
- **NumPy & Math**
- **Winsound**

---

## 📥 Installation & Running Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Air-Touch-Holographic-Calculator.git](https://github.com/YOUR_USERNAME/Air-Touch-Holographic-Calculator.git)
   cd Air-Touch-Holographic-Calculator

Install dependencies:
Make sure you have Python installed, then install the required libraries:
opencv-python
mediapipe
numpy

Ensure required files are in place:
gesture_recognizer.task (MediaPipe mogit initdel file)
icon.ico (Application window icon)

Run the application:
python app.py

🕹️ How to Use
Position yourself in front of your webcam.

Hover your Index finger over any calculator button (the button will glow yellow).

Pinch your Thumb and Index finger together to click (the button will turn green and play a click sound).

Separate your fingers to perform the next action!