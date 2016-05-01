#include <SoftwareSerial.h>
int pi1 = 10; //is invansion
int pi2 = 11; //door not closed
int pi3 = 12;
SoftwareSerial linkit7688(8,9);
SoftwareSerial linkitone(6,7);

void serial_setup(){
  pinMode(pi1,OUTPUT);
  pinMode(pi2,INPUT);
  pinMode(pi3,INPUT);
  linkit7688.begin(9600);
  linkitone.begin(9600);
}

void sendText(int object, char msg){
  //----------LinkIt One----------
  if(object == 1){
    linkitone.write(msg);
  }
  //----------part 2----------
  else if(object == 2){
    linkit7688.write(msg);
  }
  //----------part 3----------
  else if(object == 3){
    if(msg  == 'F' || msg  == 'E'){
      digitalWrite(pi3,HIGH);
    }
    if(msg  = 'S'){
      digitalWrite(pi3,LOW);
    }
  }
}

char readText(){
  if(digitalRead(pi1)){
    return 'I';
  }
  else if(digitalRead(pi2)){
    return 'D';
  }

  else if(Serial.available()){
    return Serial.read();
  }

  else{
    return 'S';
  }
}
