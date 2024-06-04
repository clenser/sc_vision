#To control led using pwm

import cv2
import mediapipe as mp
import pyfirmata2
import math



board = pyfirmata2.Arduino('COM5')
ledpin = board.get_pin('d:10:p')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
mp_drawing = mp.solutions.drawing_utils


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)  #to flip the image
    if success:
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(RGB_frame)
        if result.multi_hand_landmarks:
           hand_landmarks = result.multi_hand_landmarks[0]
           thumbTip = hand_landmarks.landmark[4]
           indexTip = hand_landmarks.landmark[8]
           distance=math.sqrt((thumbTip.x-indexTip.x)**2 + (thumbTip.y-indexTip.y)**2)
           print(distance)
           if distance < 0.042:
               ledpin.write(0)
           elif distance >0.38:
               ledpin.write(1)
           else:
              ledpin.write(distance+0.01)
           mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('capture image', frame)

        if cv2.waitKey(1) == ord('q'):
            break
cv2.destroyAllWindows()