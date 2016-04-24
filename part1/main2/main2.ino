#include <LGSM.h>
String number = "0928660419";
void setup() {
  
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial.println("Starting SMS!");
  
  while (!LSMS.ready()){
    delay(1000);
    Serial.println("Waiting for SMS");
  }
  Serial.println("Sim initialized");
  LSMS.beginSMS("0928660419");
}

void loop() {
  if(Serial1.available()){
    char c = Serial1.read();
    Serial.println(c);
    String message = "";
    if(c == 'F'){
      message  = "house is on fire";
    }
    if(c == 'E'){
      message  = "earthquake strikes";
    }
    if(c == 'G'){
      message  = "gas is leaking";
    }
    if(c == 'D'){
      message  = "door is not closed";
    }
    if(c == 'I'){
      message  = "someone enter into the house";
    }
    
    LSMS.print(message);
    if(LSMS.endSMS()){
      Serial.println("message sent successfully");
    }
    delay(20000);
  }
}
