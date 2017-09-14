#include <Wire.h>
#include <Servo.h>
Servo MOTOR1;
Servo MOTOR2;
Servo MOTOR3;
int Motors[4];
int pos = 0;
int number = 0;
int x = 0;
int y = 0;
int z = 0;
int i = 0;
void setup()
{
//  Wire.begin(0x04); // join i2c bus (address optional for master
//  Wire.onReceive(receiveEvent); // register event
//  Serial.begin(9600);           // start serial for output

  MOTOR1.attach(9);
  MOTOR2.attach(10);
  MOTOR3.attach(11);


  MOTOR1.write(92); // set servo to mid-point (90°)
  delay(2000);


}

void loop()
{
  /* myservo.write(90); // set servo to mid-point (90°)
    delay(500);
    myservo.write(90);
    delay(500);*/
   x = analogRead(5);


  x = map(x, 0, 1024, 54, 130);

  MOTOR1.write(x);

}


/*void receiveEvent(int byteCount)
{
  
  while (Wire.available())
  {
    for (int i=0; i <= 4; i++)
    {
    number = Wire.read();
    //Serial.print(number);
    Motors[i]=number;
    //Serial.println(Motors[i]);
    }

  x = Motors[1];
  x = map(x, 0, 180, 54, 130);

  y = Motors[2];
  y = map(y, 0, 180, 54, 130);

  z = Motors[3];
  z = map(z, 0, 180, 54, 130);
  
  //Serial.print(x);
  //Serial.print(y);
  //Serial.println(z);

  MOTOR1.write(x);
  MOTOR2.write(y);
  MOTOR3.write(z);
  }
}*/
