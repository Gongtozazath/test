import cv2
import serial
import time

# ตั้งค่าพอร์ต serial เพื่อเชื่อมต่อกับ Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyACM0' คือพอร์ตของ Arduino
time.sleep(2)  # รอให้การเชื่อมต่อเสถียร

# เริ่มใช้ OpenCV
cap = cv2.VideoCapture(0)  # เปิดกล้องเว็บแคม

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # แปลงเป็นภาพขาวดำเพื่อความง่ายในการประมวลผล
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Video', frame)

    # ตัวอย่างการประมวลผลภาพ เช่น ตรวจจับวัตถุและหาค่ามุมเพื่อควบคุมเซอร์โว
    # คุณสามารถปรับแต่งโค้ดนี้ให้เหมาะสมกับการใช้งานของคุณ เช่น การตรวจจับใบหน้า หรือติดตามวัตถุ
    angle = 90  # กำหนดมุมของเซอร์โว (ปรับตามเงื่อนไขที่คุณต้องการ)
    arduino.write(f"{angle}\n".encode())  # ส่งมุมไปยัง Arduino

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
