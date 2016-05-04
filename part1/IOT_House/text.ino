#include <SoftwareSerial.h>
SoftwareSerial linkitone(10,11);
SoftwareSerial linkit7688(5,9);
SoftwareSerial pi(6,7);

void serialSetup(){
  linkitone.begin(9600);
  linkit7688.begin(9600);
  pi.begin(9600);
}

void sendText(int object, String msg){
  //----------LinkIt One----------
  if(object == 1){
    linkitone.println(msg);
  }
  //----------part 2----------
  else if(object == 2){
    linkit7688.println(msg);
    Serial.println("7122");
  }
  //----------part 3----------
  else if(object == 3){
    pi.println(msg);
  }
}

String readText(){
  String content = "";
  while (pi.available()){
    content = content + (char)pi.read();
  }
  while (Serial.available()){
    content = content + (char)Serial.read();
  }
  content.trim();
  return content;
}
