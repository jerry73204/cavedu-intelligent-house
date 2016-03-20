int pin_gas_led = 3;
int pin_fan = 2;

void gas_led_setup(){
  pinMode(pin_gas_led,OUTPUT);
}

void gas_interruption(boolean power){
  
  digitalWrite(pin_gas_led,power);
}

void fan_setup(){
  pinMode(pin_fan,OUTPUT);
}

void fan(boolean power){
  digitalWrite(pin_fan,power);
}


