#include <SoftwareSerial.h>
int pi1 = 10; //is invansion
int pi2 = 11; //door not closed
int pi3 = 12; //send
SoftwareSerial linkit7688(8,9);
SoftwareSerial linkitone(6,7);
int e_event = 20;
int f_event = 21;
int g_event = 22;

int pe_value = 0;
int pf_value = 0;
int pg_value = 0;
int pIn = 0;
int pDo = 0;

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
    }
    if(msg  == 'S'){
      digitalWrite(pi3,LOW);
    }
  }
}

char readText(){
  int e_value = digitalRead(e_event);
  int f_value = digitalRead(f_event);
  int g_value = digitalRead(g_event);
  int curIn = digitalRead(pi1);
  int curDo = digitalRead(pi2);
  char result;
  
  if((e_value - pe_value) == 1){
    result = 'E';
  }
  else if((f_value - pf_value) == 1){
    result = 'F';
  }
  else if((g_value - pg_value) == 1){
    result = 'G';
  }
  else if((curIn - pIn) == 1){
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
  pe_value = e_value;
  pf_value = f_value;
  pg_value = g_value;
  pIn = curIn;
  pDo = curDo;
  
  return result;
}
