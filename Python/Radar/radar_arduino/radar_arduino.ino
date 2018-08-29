#include<Servo.h>
#include"ultrasonic.h"

/*
 * #define MIN_PULSE_WIDTH       544     // the shortest pulse sent to a servo  
*  #define MAX_PULSE_WIDTH      2400     // the longest pulse sent to a servo 
 * void writeMicroseconds(int value); //can control more precise to servo
 */
//my servo trying --> SG90 try spec
const int max_pulse_width = 2700;
const int min_pulse_width = 720;
const float maxDist = 50;
const float SG90_SPEED = 600.0; //600deg/s --> need 1.7 milliSecond to turn 1deg

//ultrasonic
const int trig = 4;
const int echo = 5;
const int usServoPin = 2;
int usServoPos = 0;
const long delayTime = 30000;
bool usDirection = true;  //true --> from 0 to 180, false --> from 180 to 0
ultrasonic* us;
Servo usServo;

//laser
const int lServoPin = 3;
const int ledPin = 13;
int lservoPos = 90;
bool lDirection = true;
Servo lServo;

void setup() {
  //initial ultrasonic and laser
  //ultrasonic
  us = new ultrasonic(trig, echo, false);
  usServo.attach(usServoPin, max_pulse_width, max_pulse_width);
  usServo.write(usServoPos);
  //laser
  pinMode(ledPin, OUTPUT);
  lServo.attach(lServoPin, max_pulse_width, max_pulse_width);
  lServo.write(lservoPos);
  //serial
  Serial.begin(115200);
}

void loop() {
  long timeMicro = micros();

  //measuring and sending ultrasonic result  
  float f;
  float f1 = us->measureDistance(24.0);
  float f2 = us->measureDistance(24.0);
  f = (f1 + f2) / 2.0f;
  f = (f<maxDist)?f:maxDist;
  
  Serial.println(String(f) + "," + String(usServoPos));

  //move ultrasonic motor
  if(usDirection){
    usServoPos += 1;
    if(usServoPos == 180){
      usDirection = false;
    } 
  } else{
    usServoPos -= 1;
    if(usServoPos == 0){
      usDirection = true;
    } 
  }
  usServo.write(usServoPos);
  
  long costTimeMicro = micros() - timeMicro;
  
  //try to make each sample time same 
  long d = delayTime - costTimeMicro;
  delayMicroseconds(d>0?d:0);
}
