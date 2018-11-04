//Ultrasonic
const int trig = 4;
const int echo = 5;

//laser
const int laserPin = 13;

//servo
#include <Servo.h>
const int USMotor = 2;
const int LMotor = 3;
Servo USServo;
Servo LServo;

//math library
#include <math.h>
#define RAD(x) x*71/4068
#define DEG(x) x*4068/71
int calcTurnDeg(float distance, float deg);
const float MAX_DIST = 40;
int turnHowMany(float distance, float deg);

void init();
float measureDistance();
void turnUSMotor(int);
void setLaser(bool);
void turnLMotor(int);
void autoPoint(int, bool);



void setup() 
{
  initial();
}

void loop() 
{
  int deg = 0;
  int degStep = 15;
  int delayTime = 1000;
  for(deg = 0; deg<=180; deg+=degStep)
  {
    turnUSMotor(deg);
    autoPoint(deg,true);
    delay(delayTime);    
  }

  for(deg = 180; deg>=0; deg-=degStep)
  {
    turnUSMotor(deg);
    autoPoint(deg,true);
    delay(delayTime);    
  }
}

void initial()
{
  //initial serial
  Serial.begin(9600);

  //initial ultrasonic
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);

  //initial Laser
  pinMode(laserPin, OUTPUT);

  //initial servo
  USServo.attach(USMotor);
  LServo.attach(LMotor);
}

float measureDistance()
{
  float duration, distance;
  digitalWrite(trig, HIGH);
  delayMicroseconds(1000);
  digitalWrite(trig, LOW);
  duration = pulseIn (echo, HIGH);
  distance = (duration/2)/29;
  return distance;  
}

void turnUSMotor(int deg)
{
  USServo.write(deg);
}

void setLaser(bool b)
{
  digitalWrite(laserPin, b?HIGH:LOW);
}

void turnLMotor(int deg)
{
  LServo.write(deg);
}

int calcTurnDeg(float distance, float deg)
{
  float d = (float)deg;
  double t = distance * sin(RAD(d)) + 4.6;
  double b = distance * cos(RAD(d));
  float degree = DEG(atan2(t, b));
  return degree;
}

int turnHowMany(float distance, float deg)
{
  if(distance <= MAX_DIST)
  {
    setLaser(true);
    return calcTurnDeg(distance, deg);
  }
  else 
  {
    setLaser(false);
    return 90;
  }
}

void autoPoint(int deg, bool ver = false)
{
  float d = measureDistance();
  int degree = turnHowMany(d, deg);
  turnLMotor(degree);
  if(ver)
  {
    Serial.println(d);
  }
}
