import cv2
import numpy as np

cap = cv2.VideoCapture(r"/Users/anu/Downloads/3059073-hd_1920_1080_24fps.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]

    roi = frame[int(height*0.6):height, 0:width]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    cv2.imshow("ROI", roi)
    cv2.imshow("ROI Edges", edges)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
