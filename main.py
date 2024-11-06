import cv2
import serial
import numpy as np
import time

# ตั้งค่าพอร์ต serial เพื่อเชื่อมต่อกับ Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyACM0' คือพอร์ตของ Arduino
time.sleep(2)  # รอให้การเชื่อมต่อเสถียร

# ฟังก์ชันส่งข้อมูลไปยัง Arduino
def send_angle(servo_index, angle):
    command = f"{servo_index} {angle}\n"
    arduino.write(command.encode())

# ฟังก์ชันสำหรับการตรวจจับมือ
def detect_hand_movement(frame):
    # แปลงภาพจาก BGR เป็น HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # หาเส้นขอบและวัตถุ
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # หากมีการตรวจพบวัตถุ
    if len(contours) > 0:
        max_contour = max(contours, key=cv2.contourArea)  # หา contour ที่มีขนาดใหญ่ที่สุด
        if cv2.contourArea(max_contour) > 1000:  # ตรวจสอบขนาดของ contour
            x, y, w, h = cv2.boundingRect(max_contour)
            center_x = x + w // 2
            center_y = y + h // 2
            return (center_x, center_y)
    
    return None

# เริ่มใช้ OpenCV
cap = cv2.VideoCapture(0)  # เปิดกล้องเว็บแคม

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # ตรวจจับการเคลื่อนไหวของมือ
    hand_position = detect_hand_movement(frame)
    
    if hand_position:
        # แสดงตำแหน่งที่ตรวจพบมือบนหน้าจอ
        cv2.circle(frame, hand_position, 10, (255, 0, 0), -1)
        
        # กำหนดมุมสำหรับเซอร์โวจากตำแหน่งของมือ (ปรับเงื่อนไขได้ตามต้องการ)
        angle = int(hand_position[0] / frame.shape[1] * 180)  # แปลงตำแหน่งแนวนอนเป็นมุม (0-180 องศา)
        send_angle(1, angle)  # ส่งมุมไปยังเซอร์โว 1
        
    cv2.imshow('Hand Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
