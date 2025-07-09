


import cv2
import mediapipe as mp
import numpy as np
import socket
import struct
import time


HOST = '1x2.12x.123.101'  
PORT = 9999
client = socket.socket()
client.connect((HOST, PORT))
print("connected to receiver!")


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
canvas = None
prev_x, prev_y = 0, 0
prev_time = time.time()
prev_swipe_x = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        index = hand.landmark[8]
        h, w, _ = frame.shape
        x, y = int(index.x * w), int(index.y * h)

        
        if prev_x == 0 and prev_y == 0:
            prev_x, prev_y = x, y
        cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 0, 255), 4)
        prev_x, prev_y = x, y

        current_time = time.time()
        if prev_swipe_x is not None:
            dx = abs(x - prev_swipe_x)
            dt = current_time - prev_time
            speed = dx / dt if dt > 0 else 0

            if speed > 800: 
                print("swipe detected — sending drawing bro!")
                _, buffer = cv2.imencode('.jpg', canvas)
                data = buffer.tobytes()
                size = len(data)

                try:
                    client.sendall(struct.pack('>L', size) + data)
                    print("sent drawing!")
                except:
                    print("connection error")
                    break

        prev_swipe_x = x
        prev_time = current_time
    else:
        prev_x, prev_y = 0, 0

    cv2.imshow("live drawing", canvas)
    cv2.imshow("your camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
client.close()
cv2.destroyAllWindows()





