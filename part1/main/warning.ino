int pin_buzz = 3;

void warning_setup(){
  pinMode(pin_buzz,OUTPUT);
}
void buzzE(){
  for(int i = 0;i < 7;i++){
      digitalWrite(pin_buzz,HIGH);
      delay(200);
      digitalWrite(pin_buzz,LOW);
      delay(200);
      digitalWrite(pin_buzz,HIGH);
      delay(200);
      digitalWrite(pin_buzz,LOW);
      delay(200);
      digitalWrite(pin_buzz,HIGH);
      delay(200);
      digitalWrite(pin_buzz,LOW);
      delay(400);
  }
}
void buzzF(){
  for(int i = 0;i < 10;i++){
      digitalWrite(pin_buzz,HIGH);
      delay(200);
      digitalWrite(pin_buzz,LOW);
      delay(200);
      digitalWrite(pin_buzz,HIGH);
      delay(200);
      digitalWrite(pin_buzz,LOW);
      delay(400);
  }
}
void buzzG(){
  for(int i = 0;i < 6;i++){
      digitalWrite(pin_buzz,HIGH);
      delay(200);
      digitalWrite(pin_buzz,LOW);
      delay(200);
      digitalWrite(pin_buzz,HIGH);
      delay(200);
      digitalWrite(pin_buzz,LOW);
      delay(400);
      digitalWrite(pin_buzz,HIGH);
      delay(200);
      digitalWrite(pin_buzz,LOW);
      delay(400);
  }
}
void buzzI(){
  for(int i = 0;i < 33;i++){
      digitalWrite(pin_buzz,HIGH);
      delay(200);
      digitalWrite(pin_buzz,LOW);
      delay(100);
  }
}
void buzzD(){
  for(int i = 0;i < 16;i++){
      digitalWrite(pin_buzz,HIGH);
      delay(400);
      digitalWrite(pin_buzz,LOW);
      delay(200);
  }
}
