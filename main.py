import cv2
import serial
import mediapipe as mp
import time

# ตั้งค่าพอร์ต serial เพื่อเชื่อมต่อกับ Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyACM0' คือพอร์ตของ Arduino
time.sleep(2)  # รอให้การเชื่อมต่อเสถียร

# ฟังก์ชันส่งข้อมูลไปยัง Arduino
def send_angle(servo_index, angle):
    command = f"{servo_index} {angle}\n"
    arduino.write(command.encode())

# ตั้งค่า Mediapipe สำหรับการตรวจจับมือ
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# เริ่มใช้ OpenCV
cap = cv2.VideoCapture(0)  # เปิดกล้องเว็บแคม

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # ตรวจจับตำแหน่งที่สนใจ (เช่น ข้อมือ, ข้อนิ้ว)
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            wrist_x = int(wrist.x * frame.shape[1])
            wrist_y = int(wrist.y * frame.shape[0])

            # วาดจุดข้อมือ
            cv2.circle(frame, (wrist_x, wrist_y), 10, (255, 0, 0), -1)

            # คำนวณมุมสำหรับเซอร์โวจากตำแหน่งของข้อมือ
            angle = int(wrist_x / frame.shape[1] * 180)  # แปลงตำแหน่งแนวนอนเป็นมุม (0-180 องศา)
            send_angle(1, angle)  # ส่งมุมไปยังเซอร์โว 1

    cv2.imshow('Hand and Arm Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
