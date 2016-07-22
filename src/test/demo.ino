#define VERSION     "\n\nGripper demo V1.2- @kas2014\n"

// V1.2  use VarSpeedServo library
// V1.1  2 servo's
// V1.0  1 servo

#include <VarSpeedServo.h> 

#define    rot_pin              10                  // Green
#define    pinch_pin             9                  // Yellow

#define    CLOSE                85                  // servo's limits
#define    OPEN                132
#define    CW                    0
#define    MID                  87
#define    CCW                 171

#define    SLOW                 30
#define    FAST                 80

VarSpeedServo pinch_servo;                          // create servo objects
VarSpeedServo rot_servo;

void setup()  {
  pinch_servo.attach(pinch_pin);  
  rot_servo.attach(rot_pin, 580, 2570);
  gripOpen(FAST);
  armCenter(FAST);
  delay(500);
}

void loop() {
  for(int i=0; i<3; i++)  {
    gripClose(SLOW);
    armRight(SLOW);
    gripOpen(SLOW);
    armCenter(SLOW);
  }
  delay(500);

  for(int i=0; i<3; i++)  {
    gripClose(FAST);
    armRight(FAST);
    gripOpen(FAST);
    armCenter(FAST);
  }
  delay(500);

  for(int i=0; i<2; i++)  {
    gripClose(SLOW);
    armLeft(SLOW);
    gripOpen(SLOW);
    armCenter(SLOW);
  }
  while(true);
} 

void armRight(int speed)    { rot_servo.write(CW, speed, true); }
void armLeft(int speed)     { rot_servo.write(CCW, speed, true); }
void armCenter(int speed)   { rot_servo.write(MID, speed, true); }
void gripOpen(int speed)    { pinch_servo.write(OPEN, speed, true); }
void gripClose(int speed)   { pinch_servo.write(CLOSE, speed, true); }
