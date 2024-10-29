import cv2
import mediapipe as mp
import pyautogui

# Initialize the webcam and face mesh detector
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Check if the webcam opened successfully
if not cam.isOpened():
    print("Error: Camera could not be opened.")
    exit()

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Flip the frame for better user interaction
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect facial landmarks
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks

    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Draw landmarks for controlling mouse movement
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)  # Green circle for eye landmarks

            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)

        # Detect eye blink using specific landmarks
        left_eye_landmarks = [landmarks[145], landmarks[159]]  # Key eye landmarks for blink detection
        for landmark in left_eye_landmarks:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)  # Yellow circles for blink detection

        # Blink detection logic based on y-coordinate difference
        if (left_eye_landmarks[0].y - left_eye_landmarks[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1)

    # Show the frame with drawn landmarks
    cv2.imshow('Eye Controlled Mouse', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the windows
cam.release()
cv2.destroyAllWindows()
