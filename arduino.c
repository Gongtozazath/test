#include <Servo.h>

Servo servo1;

void setup() {
  servo1.attach(9); // ต่อเซอร์โวที่ขา PWM 9
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    int angle = Serial.parseInt(); // อ่านมุมที่รับจาก Raspberry Pi
    if (angle >= 0 && angle <= 180) {
      servo1.write(angle); // ขยับเซอร์โวไปยังมุมที่กำหนด
    }
  }
}
