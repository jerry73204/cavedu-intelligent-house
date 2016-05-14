int pin_gas_handdle = 4;
int pin_door_open = 2;

void handdle_setup(){
  pinMode(pin_gas_handdle,OUTPUT);
  pinMode(pin_door_open,OUTPUT);
}

void gas(boolean power){
  digitalWrite(pin_gas_handdle,power);
}

void door(boolean power){
  digitalWrite(pin_door_open,power);
}



