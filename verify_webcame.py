import cv2
cam = cv2.VideoCapture(0)
if cam.isOpened():
    print("Webcam is working.")
else:
    print("Webcam could not be opened.")
cam.release()
