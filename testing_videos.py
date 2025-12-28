import cv2

videos = [r"/Users/anu/Downloads/vecteezy_view-along-the-way-on-road-1081-from-nan-province-to-bo_7223764.mp4"]

for video in videos:
    cap = cv2.VideoCapture(f"videos/{video}")
    print("Testing:", video)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Testing Video", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()

cv2.destroyAllWindows()
