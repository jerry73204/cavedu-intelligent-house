int pin_buzz = 2;
int pin_light = 13;

void buzz(boolean power){
  pinMode(pin_buzz,OUTPUT);
  digitalWrite(pin_buzz,power);
}

void warring_light(boolean power){
  pinMode(pin_light,OUTPUT);
  digitalWrite(pin_light,power);
}

void LCD(String text){
  
}
