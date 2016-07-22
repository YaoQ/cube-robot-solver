#define VERSION       "Cube Mover V1.2  @kas2014\n"

// V1.2: refactored using Cube class
// V1.1: replaced Servo with VarSpeedServo library 
// V1.0: initial release

#include <VarSpeedServo.h> 
#include "cube.h"

// ---------- user adjustments -------------------
#define    DOWN_CLOSE          91 //92
#define    DOWN_OPEN          132
#define    DOWN_CW              6
#define    DOWN_MID            89
#define    DOWN_CCW           172

#define    BACK_CLOSE          84 //85
#define    BACK_OPEN          129
#define    BACK_CW              2
#define    BACK_MID            87
#define    BACK_CCW           171

#define    LOW_SPEED           50 //50
#define    HI_SPEED           100 //80
// -----------------------------------------------

#define    downPinchPin         9
#define    downRotPin          10
#define    backPinchPin         5
#define    backRotPin           6
#define    bipPin              11             // buzzer
#define    myRX                 2
#define    myTX                 3

#define    STX               0x02             // serial data frame delimiters
#define    ETX               0x03

Cube myCube(downPinchPin, downRotPin, backPinchPin, backRotPin);

char cmd[128];                                 // bytes received buffer

void setup() {
  Serial.begin(57600);
  Serial.println(VERSION);
  pinMode(bipPin, OUTPUT);     

  myCube.begin(HI_SPEED);                 // set HIGH servo's speed 
  myCube.downSetLimits(DOWN_CLOSE, DOWN_OPEN, DOWN_CW,DOWN_MID, DOWN_CCW); // set limits for pinch and rotation servo's
  myCube.backSetLimits(BACK_CLOSE, BACK_OPEN, BACK_CW, BACK_MID, BACK_CCW);
  myCube.seize();
  bip(20, 2);                             // bip
}

void loop() {
  if(getSerialData())       parseData(); 
}

// ---------------------------

boolean getSerialData()  {
  if(Serial.available())  {                           // data received from smartphone
    delay(2);
    cmd[0] =  Serial.read();  
    if(cmd[0] == STX)  {
      int i=1;      
      while(Serial.available())  {
        delay(1);
        cmd[i] = Serial.read();
//      Serial.print(cmd[i]);
        if(cmd[i]>'u' || i>124)    {  bip(20, 5);    return false; }    // Communication error  XXX reinitialiser à zero <<<
        if((cmd[i]==ETX))               return true;     // 
        i++;
      }
    }
  }
 return false; 
}

boolean getSerialMonitor()  {  // Serial Monitor fsetting: Newline
  if(Serial.available())  {
    for(int i=0; i<124; i++)    cmd[i] = 0;
    int n = Serial.readBytesUntil('\n', cmd, 124);
//   Serial.print(cmd[0]); Serial.print(" ");
   cmd[n+1] = ETX;
   return true;
  }
 return false; 
}

void parseData()    { // parseData(cmd)
  int i = 0;
  String progress = "";
  while (cmd[i] != ETX) {
//  Serial.print(cmd[i]); mySerial.print(" ");
    switch(cmd[i])  {

      // Move commands  ------------------------------------------------------------
      case 'R':                                                    //  'R' moves
        switch(cmd[i+1])  {
          case '2':
            Serial.print("R2 ");
            myCube.R2();
            break;
          case 39:
            Serial.print("R' ");
            myCube.Rp();
            break;
          default:
            Serial.print("R ");
            myCube.R();
            break;
        }
        break;
      case 'L':                                                    //  'L' moves
        switch(cmd[i+1])  {
          case '2':
            Serial.print("L2 ");
            myCube.L2();
            break;
          case 39:
            Serial.print("L' ");
            myCube.Lp();
            break;
          default:
            Serial.print("L ");
            myCube.L();
            break;
        }
        break;
      case 'U':                                                    //  'U' moves
        switch(cmd[i+1])  {
          case '2':
            Serial.print("U2 ");
            myCube.U2();
            break;
          case 39:
            Serial.print("U' ");
            myCube.Up();
            break;
          default:
            Serial.print("U ");
            myCube.U();
            break;
        }
        break;
      case 'D':       ** snip (9000 caracters limitation) **
      case 'F': 
      case 'B':
       }
        break;

      // Scan commands  -----------------------------------------------------------
      case 'f':                                             // Scan Front side
        myCube.scanFront();
        Serial.println("OKf");
        break;
      case 'r':                                            // Scan Right side
        myCube.scanRight();
        Serial.println("OKr");
        break;
      case 'b':                                            // Scan Back side
        myCube.scanBack();
        Serial.println("OKb");
        break;
      case 'l':                                            // Scan Right side
        myCube.scanLeft();
        Serial.println("OKl");
        break;
      case 'u':                                            // Scan Up side
        myCube.scanUp();
        Serial.println("OKu");
        break;
      case 'd':                                            // Scan Down side
        myCube.scanDown();
        Serial.println("OKd");
        break;
      case 'g':                                           // back to Front side
        myCube.scanFront2();
        Serial.println("OKg");
        break;

      // Other commands  --------------------------------------------------------------
      case 'T':                                          // release gripper pressure
        myCube.seize();
        bip(40, 2);
        Serial.print("seize");
        break;
      case 'S':                                         // change move speed
        switch(cmd[i+1])  {
          case '2':
            myCube.setSpeed(HI_SPEED);
            Serial.print("High Speed");
            break;
          case '1':
            myCube.setSpeed(LOW_SPEED);
            Serial.print("Low Speed");
            break;
        }
        break;
      case 'V':                                         // bips
        switch(cmd[i+1])  {
          case '4':
            bip(80, 4);
            Serial.print("bip (4)");
            break;
          case '2':
            bip(80, 2);
            Serial.print("bip (2)");
            break;
          default:
            bip(80, 1);
            Serial.print("bip ");
            break;
        }
        break;

      default:
          break;
      }
      i++;
  }
  Serial.println();
  bip(20, 2);
}

void bip(int duration, int n)    {            // Bip piezo: duration in ms, n repeats
  for(int i=0; i<n; i++)  {  
     digitalWrite(bipPin, HIGH);        
     delay(duration);
     digitalWrite(bipPin, LOW);         
     delay(75);
  }
}
