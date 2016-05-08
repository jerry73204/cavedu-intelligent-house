#include <LGSM.h>
String number = "0919220341";
int pinE = 5;
int pinF = 6;
int pinG = 7;

void setup() {

//  Serial.begin(9600);
  Serial1.begin(9600);
//  Serial.println("Starting SMS!");

  pinMode(pinE,OUTPUT);
  pinMode(pinF,OUTPUT);
  pinMode(pinG,OUTPUT);

  while (!LSMS.ready()){
    delay(1000);
//    Serial.println("Waiting for SMS");
  }
//  Serial.println("Sim initialized");
  LSMS.beginSMS("0928660419");
}

void loop() {
  if(Serial1.available()){
    char c = Serial1.read();
//    Serial.println(c);
    if(c != 'S'){
      String message = "";
      if(c == 'F'){
        digitalWrite(pinF,HIGH);
        message  = "house is on fire";
      }
      else if(c == 'E'){
        digitalWrite(pinE,HIGH);
        message  = "there is an earthquake";
      }
      else if(c == 'G'){
        digitalWrite(pinG,HIGH);
        message  = "gas is leaking";
      }
      else if(c == 'D'){
        message  = "door is not closed";
      }
      else if(c == 'I'){
        message  = "someone enter into the house";
      }

      LSMS.print(message);
      LSMS.endSMS();
    }
    else{
      digitalWrite(pinE,LOW);
      digitalWrite(pinF,LOW);
      digitalWrite(pinG,LOW);
    }
  }
}
