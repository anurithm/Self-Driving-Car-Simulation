import cv2
import numpy as np

def detect_edges(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges

def region_of_interest(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)

    polygon = np.array([
        [(0, height),
         (width, height),
         (width, int(height*0.6)),
         (0, int(height*0.6))]
    ], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    return cv2.bitwise_and(edges, mask)

def detect_lines(roi_edges):
    lines = cv2.HoughLinesP(
        roi_edges,
        rho=1,
        theta=np.pi/180,
        threshold=100,
        minLineLength=40,
        maxLineGap=150
    )
    return lines

def steering_logic(lines):
    if lines is None:
        return "STOP"
    return "GO STRAIGHT"

cap = cv2.VideoCapture(r"/Users/anu/Downloads/3059073-hd_1920_1080_24fps.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    edges = detect_edges(frame)
    roi = region_of_interest(edges)
    lines = detect_lines(roi)

    direction = steering_logic(lines)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1,y1), (x2,y2), (0,255,0), 3)

    cv2.putText(
        frame,
        direction,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.imshow("Self Driving Car Simulation", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
