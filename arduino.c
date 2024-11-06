#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

void setup() {
  servo1.attach(9);  // ต่อเซอร์โวที่ขา PWM 9
  servo2.attach(10); // ต่อเซอร์โวที่ขา PWM 10
  servo3.attach(11); // ต่อเซอร์โวที่ขา PWM 11
  servo4.attach(12); // ต่อเซอร์โวที่ขา PWM 12
  servo5.attach(5);  // ต่อเซอร์โวที่ขา PWM 5
  servo6.attach(6);  // ต่อเซอร์โวที่ขา PWM 6

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // อ่านข้อมูลมุมจาก Raspberry Pi
    int servoIndex = Serial.parseInt(); // อ่านหมายเลขเซอร์โว (1-6)
    int angle = Serial.parseInt();      // อ่านมุมที่จะขยับ (0-180)

    // ตรวจสอบว่าหมายเลขเซอร์โวและมุมถูกต้อง
    if (servoIndex >= 1 && servoIndex <= 6 && angle >= 0 && angle <= 180) {
      switch (servoIndex) {
        case 1: servo1.write(angle); break;
        case 2: servo2.write(angle); break;
        case 3: servo3.write(angle); break;
        case 4: servo4.write(angle); break;
        case 5: servo5.write(angle); break;
        case 6: servo6.write(angle); break;
      }
    }
  }
}
