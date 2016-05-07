#include <SoftwareSerial.h>
int pi1 = 10; //is invansion
int pi2 = 11; //door not closed
int pi3 = 12; //send
SoftwareSerial linkit7688(8,9);
SoftwareSerial linkitone(6,7);

void serial_setup(){
  pinMode(pi1,INPUT);
  pinMode(pi2,INPUT);
  pinMode(pi3,OUTPUT);
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
      Serial.println("J");
    }
    if(msg  == 'S'){
      digitalWrite(pi3,LOW);
      Serial.println("J");
    }
  }
}

int pIn = 0;
int pDo = 0;

char readText(){
  int curIn = digitalRead(pi1);
  int curDo = digitalRead(pi2);
  char result;
  if((curIn - pIn) == 1){
    result = 'I';
  }
  else if((curDo - pDo) == 1){
    result = 'D';
  }
  
  else if(Serial.available()){
    result =  Serial.read();
  }
  else{
    result = 'S';
  }
  pIn = curIn;
  pDo = curDo;
  return result;
}
