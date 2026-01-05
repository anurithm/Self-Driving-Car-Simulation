import streamlit as st
import cv2
import numpy as np
from tempfile import NamedTemporaryFile

# ------------------ Functions ------------------

def detect_edges(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges

def region_of_interest(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)

    polygon = np.array([[
        (0, height),
        (width, height),
        (width//2, height//2)
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    return cv2.bitwise_and(edges, mask)

def detect_lines(frame, edges):
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi/180,
        threshold=100,
        minLineLength=50,
        maxLineGap=150
    )

    line_img = np.zeros_like(frame)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 5)

    return cv2.addWeighted(frame, 0.8, line_img, 1, 1)

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Self-Driving Car Simulation", layout="centered")

st.title("🚗 Self-Driving Car Simulation")
st.write("Upload a road video to visualize lane detection.")

uploaded_file = st.file_uploader(
    "Choose a road video",
    type=["mp4", "avi"]
)

if uploaded_file is not None:
    tfile = NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    cap = cv2.VideoCapture(tfile.name)
    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        edges = detect_edges(frame)
        roi = region_of_interest(edges)
        output = detect_lines(frame, roi)

        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        stframe.image(output, channels="RGB")

    cap.release()
