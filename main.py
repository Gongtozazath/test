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
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            elbow = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]  # จุดสมมุติใกล้ศอก

            # คำนวณตำแหน่งสำหรับจุดต่างๆ
            wrist_x = int(wrist.x * frame.shape[1])
            wrist_y = int(wrist.y * frame.shape[0])
            index_x = int(index_finger.x * frame.shape[1])
            index_y = int(index_finger.y * frame.shape[0])
            elbow_x = int(elbow.x * frame.shape[1])
            elbow_y = int(elbow.y * frame.shape[0])

            # วาดจุดต่างๆ
            cv2.circle(frame, (wrist_x, wrist_y), 10, (255, 0, 0), -1)
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)
            cv2.circle(frame, (elbow_x, elbow_y), 10, (0, 0, 255), -1)

            # คำนวณมุมหรือระยะห่างสำหรับเซอร์โวจากตำแหน่งที่ตรวจจับได้
            angle_wrist = int(wrist_x / frame.shape[1] * 180)
            angle_index = int(index_y / frame.shape[0] * 180)
            send_angle(1, angle_wrist)  # ส่งมุมไปยังเซอร์โว 1
            send_angle(2, angle_index)  # ส่งมุมไปยังเซอร์โว 2

    cv2.imshow('Hand and Arm Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
