int pin_buzz = 3;

void warning_setup(){
  pinMode(pin_buzz,OUTPUT);
}
void buzz(){
  for(int i = 0;i < 10;i++){
      digitalWrite(pin_buzz,HIGH);
      delay(500);
      digitalWrite(pin_buzz,LOW);
      delay(500);
  }
}
