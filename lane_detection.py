import cv2

cap = cv2.VideoCapture(r"/Users/anu/Downloads/3059073-hd_1920_1080_24fps.mp4")

if not cap.isOpened():
    print("Error: Could not open video file")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray Video", gray)

    if cv2.waitKey(1) == 27:  # Press Esc to exit
        break

cap.release()
cv2.destroyAllWindows()
