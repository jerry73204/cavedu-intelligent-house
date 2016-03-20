int pin_buzz = 4;
int pin_light = 5;

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
