import streamlit as st
import cv2
import numpy as np
from tempfile import NamedTemporaryFile

# Title
st.title("Self-Driving Car Simulation 🚗")
st.write("Upload a road video and simulate lane detection and steering logic.")

# Upload video
uploaded_file = st.file_uploader("Choose a video...", type=["mp4","avi"])

if uploaded_file is not None:
    # Save uploaded video temporarily
    tfile = NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    # Open video
    cap = cv2.VideoCapture(tfile.name)

    stframe = st.empty()  # placeholder for video frames

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # --- Lane detection ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        # ROI
        height, width = edges.shape
        mask = np.zeros_like(edges)
        polygon = np.array([[
            (0, height),
            (width, height),
            (width, int(height*0.6)),
            (0, int(height*0.6))
        ]], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        roi_edges = cv2.bitwise_and(edges, mask)

        # Hough Lines
        lines = cv2.HoughLinesP(roi_edges, 1, np.pi/180, 100, minLineLength=40, maxLineGap=150)
        direction = "STOP" if lines is None else "GO STRAIGHT"

        # Draw lines
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1,y1), (x2,y2), (0,255,0), 3)

        # Put steering text
        cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        # Convert BGR to RGB for Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    cap.release()
