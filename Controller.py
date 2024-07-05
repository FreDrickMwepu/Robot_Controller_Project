# AUTHOR: FREDRICK MWEPU
# DATE: 13/06/2024

import cv2
import pyfirmata
from cvzone.HandTrackingModule import HandDetector


# Initialize communication with Arduino
comport = '/dev/tty.usbmodem00001'  # Replace with the correct port for your system
board = pyfirmata.Arduino(comport)

# Define the motor control pins on the Arduino board for L298N motor driver module
ENA = board.get_pin('d:5:p')
ENB = board.get_pin('d:6:p')
IN1 = board.get_pin('d:7:o')
IN2 = board.get_pin('d:8:o')
IN3 = board.get_pin('d:9:o')
IN4 = board.get_pin('d:11:o')

# Function to control the motors based on the number of fingers up
def control_car(fingerUp):
    # Stop the car
    if fingerUp == [0, 0, 0, 0, 0]:
        ENA.write(0)
        ENB.write(0)
        IN1.write(0)
        IN2.write(0)
        IN3.write(0)
        IN4.write(0)
    # Move forward
    elif fingerUp == [0, 1, 0, 0, 0]:
        ENA.write(1)
        ENB.write(1)
        IN1.write(1)
        IN2.write(0)
        IN3.write(1)
        IN4.write(0)
    # Move backward
    elif fingerUp == [0, 1, 1, 0, 0]:
        ENA.write(1)
        ENB.write(1)
        IN1.write(0)
        IN2.write(1)
        IN3.write(0)
        IN4.write(1)
    # Turn left
    elif fingerUp == [0, 1, 1, 1, 0]:
        ENA.write(1)
        ENB.write(1)
        IN1.write(0)
        IN2.write(1)
        IN3.write(1)
        IN4.write(0)
    # Turn right
    elif fingerUp == [0, 1, 1, 1, 1]:
        ENA.write(1)
        ENB.write(1)
        IN1.write(1)
        IN2.write(0)
        IN3.write(0)
        IN4.write(1)

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Start the video capture
video = cv2.VideoCapture(1)

# Main loop to detect the number of fingers up and control the car
try:
    while True:
        ret, frame = video.read()
        # Break the loop if no frame is captured
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        hands, img = detector.findHands(frame)
        # Get the list of fingers up
        if hands:
            lmList = hands[0]
            fingerUp = detector.fingersUp(lmList)
            # Display the number of fingers up on the screen
            print(fingerUp)
            control_car(fingerUp)
            if fingerUp == [0, 0, 0, 0, 0]:
                cv2.putText(frame, 'Finger count: 0', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            elif fingerUp == [0, 1, 0, 0, 0]:
                cv2.putText(frame, 'Finger count: 1', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            elif fingerUp == [0, 1, 1, 0, 0]:
                cv2.putText(frame, 'Finger count: 2', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            elif fingerUp == [0, 1, 1, 1, 0]:
                cv2.putText(frame, 'Finger count: 3', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            elif fingerUp == [0, 1, 1, 1, 1]:
                cv2.putText(frame, 'Finger count: 4', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            elif fingerUp == [1, 1, 1, 1, 1]:
                cv2.putText(frame, 'Finger count: 5', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

        # Display the frame
        cv2.imshow("frame", frame)
        k = cv2.waitKey(1)
        if k == ord("k"):
            break
finally:
    video.release()
    cv2.destroyAllWindows()
    board.exit()
