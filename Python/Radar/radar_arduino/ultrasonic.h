#include<NewPing.h>

class ultrasonic{
public:
  ultrasonic(){
      
  }
  
  ultrasonic(int t, int e, bool useNew=false){
	this->useNewPing = useNew;
	if(useNew){
	  sonar = new NewPing(t, e, 200);
	}
    this->trig = t;
    this->echo = e;
    pinMode (this->trig, OUTPUT);
    pinMode (this->echo, INPUT);  
  }
  
  float measureDistance(float f = 15.0){
	if(useNewPing){
	  return sonar->ping_cm();
	} else{
      return measureDistanceOld(f);
	} 
  }

  float measureDistanceOld(float deg=15.0){
    float c = 331.0f + 0.6f * deg;
    float d = 10000.0f/c;
	float duration;
    float distance;
    digitalWrite(trig, HIGH);
    delayMicroseconds(this->delayMicroTime);
    digitalWrite(trig, LOW);
    duration = pulseIn (echo, HIGH, 15000); //15000us can measure 2.55m at temp=15deg
	if(duration != 0){
		distance = (duration/2.0f)/d;
	} else {
		distance = 250.0f;
	}
    return distance;
  }
  
  long delayTime(){
	  return delayMicroTime;
  }

private:
  int trig;
  int echo;
  bool useNewPing;
  NewPing* sonar;
  static const long delayMicroTime;
};

static const long ultrasonic::delayMicroTime = 1000;