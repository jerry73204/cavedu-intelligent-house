int pin_buzz = 3;
int pin_gas = 0;
int pin_fire = 1;
int pin_earthquake = 2;

void warning_setup(){
  pinMode(pin_buzz,OUTPUT);
  pinMode(pin_gas,OUTPUT);
  pinMode(pin_fire,OUTPUT);
  pinMode(pin_earthquake,OUTPUT);
}
void buzz(boolean power){
  digitalWrite(pin_buzz,power);
}

void warring_fire(boolean power){
  digitalWrite(pin_fire,power);
}

void warring_gas(boolean power){
  digitalWrite(pin_gas,power);
}

void warring_earthquake(boolean power){
  digitalWrite(pin_earthquake,power);
}
