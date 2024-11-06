import cv2
import serial
import time

# ตั้งค่าพอร์ต serial เพื่อเชื่อมต่อกับ Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyACM0' คือพอร์ตของ Arduino
time.sleep(2)  # รอให้การเชื่อมต่อเสถียร

# เริ่มใช้ OpenCV
cap = cv2.VideoCapture(0)  # เปิดกล้องเว็บแคม

# ฟังก์ชันส่งข้อมูลไปยัง Arduino
def send_angle(servo_index, angle):
    command = f"{servo_index} {angle}\n"
    arduino.write(command.encode())

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # แปลงเป็นภาพขาวดำเพื่อความง่ายในการประมวลผล
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Video', frame)

    # ตัวอย่างการประมวลผลภาพ เช่น การกำหนดค่ามุมสำหรับเซอร์โวแต่ละตัว
    # คุณสามารถเขียนเงื่อนไขการควบคุมเพิ่มเติมได้ตามที่คุณต้องการ
    angles = [90, 45, 30, 60, 120, 150]  # ตัวอย่างค่ามุมสำหรับเซอร์โว 6 ตัว

    # ส่งมุมไปยัง Arduino
    for i in range(6):
        send_angle(i + 1, angles[i])  # ส่งหมายเลขเซอร์โว (1-6) และมุม

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
