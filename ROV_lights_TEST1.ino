#include <Wire.h>
#include <Servo.h>
#include <OneWire.h>
#include <DallasTemperature.h>
Servo MOTOR1;
Servo MOTOR2;
Servo MOTOR3;
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
int Motors[5];//4-5
int pos = 0;
int number = 0;
int x = 0;
int y = 0;
int z = 0;
int i = 0;
int a = 0;
int b = 0;
int t1 = 0;
int t2 = 0;
int t3 = 0;
int t4 = 0;
int t5 = 0;
int Status = 0;
float e = 0;//analogRead(1)
float r = 0;//analogRead(2)
float t = 0;//analogRead(3)
float s = 0;//Battery cell 1
float d = 0;//Battery cell 2
float f = 0;//Battery cell 3
long timeThis, timeLast;

void setup()
{

  Wire.begin(0x04); // join i2c bus (address optional for master
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
  analogReference(INTERNAL);// sets it to read 1.1V
  Wire.beginTransmission(0x01);
  //Wire.onRequest(RequestData);
  sensors.begin();

  MOTOR1.attach(9);
  MOTOR2.attach(10);
  MOTOR3.attach(11);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);

  MOTOR1.write(90); // set servo to mid-point (90°)
  delay(2000);


  digitalWrite(3, LOW);
  digitalWrite(4, LOW);


}

void loop()
{
  timeThis = millis();
  if (timeThis - timeLast >= 10000) {
    Serial.println("count!");
    //Store the present count of millis in the last count
    timeLast = timeThis;
    sensors.requestTemperatures();

    t1 = sensors.getTempCByIndex(0); // Why "byIndex"?
    t2 = sensors.getTempCByIndex(1);
    t3 = sensors.getTempCByIndex(2);
    t4 = sensors.getTempCByIndex(3);
    t5 = sensors.getTempCByIndex(4);
   
  }

    Serial.print(t1);
    Serial.print(',');
    Serial.print(t2);
    Serial.print(',');
    Serial.print(t3);
    Serial.print(',');
    Serial.print(t4);
    Serial.print(',');
    Serial.print(t5);
    Serial.print(',');
    
  //sensors.requestTemperatures();
  /* myservo.write(90); // set servo to mid-point (90°)
    delay(500);
    myservo.write(90);
    delay(500);*/
  // x = analogRead(5);


  // x = map(x, 0, 1024, 54, 130);

  // MOTOR1.write(x);

  e = analogRead(1);
  r = analogRead(2);
  t = analogRead(3);

  //------------------------Cell 1--------------------------------------
  /*
    //e = map(e, 0, 1023, 0, 92);
    //e = map(e, 0, 92, 0, 370);
    e = map(e, 0, 1023, 0, 370);//e, 0, 1023, 0, 370
    e = e / 100;
  */

  //s = e * 4.2;
  //s = s / 969;//equation for Battery cell 1

  //e = e / 276.48;
  e = e / 930;// the factor ratio, this determines what Vin is. The Factor ratio is how we get from 0-1023 to the 0-1.1V that the Arduino is reading.
  e = (e * 13300) / 3300; // this is the equation for Vin when we know Vin.
  // The equation is Vin=(Vout(R2+R1))/R2
  // the reverse is Vout=Vin*R2/(R1+R2)
  // This in its entirety simply converts the 0-1.1V to 0-3.7V, this is the same process for the other ones


  s = e;

  //------------------------Cell 2--------------------------------------
  /*
    //r = map(r, 0, 1023, 0, 111);//r, 0, 1023, 0, 97
    //r = map(r, 0, 111, 0, 740);//r, 0, 97, 0, 740
    r = map(r, 0, 1023, 0, 740);//r, 0, 1023, 0, 740
    r = r / 100;
  */

  //d = r * 4.2;
  //d = d / 969;//equation for Battery cell 2

  r = r / 930;
  r = (r * 11500) / 1500;

  r = r - s;
  d = r;

  //------------------------Cell 3--------------------------------------
  /*
    //t = map(t, 0, 1023, 0, 111);//t, 0, 1023, 0, 101
    //t = map(t, 0, 111, 0, 1110);//t, 0, 101, 0, 1110
    t = map(t, 0, 1023, 0, 1110);//t, 0, 1023, 0, 1110
    t = t / 100;
  */

  //s = e * 4.2;
  //f = f/ 969;//equation for Battery cell 3

  t = t / 930;
  t = (t * 11000) / 1000;

  t = t - r;
  t = t - s;
  f = t;

  //--------------------------------------------------------------

  Serial.print(s);//Battery cell 1
  Serial.print(',');
  Serial.print(d);//Battery cell 2
  Serial.print(',');
  Serial.println(f);//Battery cell 3
  Serial.print(',');


}




void receiveEvent(int byteCount)
{

  while (Wire.available())
  {
    for (int i = 0; i <= 5; i++)
    {
      number = Wire.read();
      //Serial.print(number);
      Motors[i] = number;
      //Serial.println(Motors[i]);
    }

    if (Motors[0] == 4 and Motors[1] == -1) {
      RequestData();
      //Serial.println("requesting");
    }
    if (Motors[0] == 5) {
      Status = 1;
      //Serial.println("Status=1");
    }
    //Serial.println(',');

    //Serial.print(x);
    //Serial.print(y);
    //Serial.println(z);

    if (Status == 1) {
      x = Motors[1];
      x = map(x, 0, 180, 54, 130);

      y = Motors[2];
      y = map(y, 0, 180, 54, 130);

      z = Motors[3];
      z = map(z, 0, 180, 54, 130);

      a = Motors[4];
      a = a - 1;
      a = !a;
      b = Motors[5];
      b = b - 1;
      b = !b;



      MOTOR1.write(x);
      MOTOR2.write(y);
      MOTOR3.write(z);

      //Serial.print(a);
      //Serial.println(b);

      if (a == 1) {
        digitalWrite(3, HIGH);
        digitalWrite(4, HIGH);
      }
      if (b == 1) {
        digitalWrite(3, LOW);
        digitalWrite(4, LOW);
      }
    }
  }
}

void RequestData()
{
  //Serial.println("Status=2");
  Status = 2;

  /*if (f > 3.00 and f < 4.40  ) {

    Wire.write('Good');
    }

    else{
    Wire.write('Bad');
    }
  */

  //Serial.write(12);
  //Wire.write(12);
  //Wire.write(b);
  //Wire.write(s);
  //Wire.write(d);
  //Wire.write(f);
}




