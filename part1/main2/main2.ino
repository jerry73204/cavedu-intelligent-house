/*
 * Copyright (C) HENNES CO., LTD. - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written in May 2016 by
 * Li-Wei Shih
 * Hao-Yun Hsueh
 * Feng-Chih Hsu
 * Hsiang-Jiu Lin
 * Cheng-Chang Liu
 * Pei-Hsuan Yan
 */
#include <LGSM.h>
#define number "0928660419"
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
      LSMS.beginSMS(number);
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
