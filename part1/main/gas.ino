int pin_gas_handdle = 4;

void gas_setup(){
  pinMode(pin_gas_handdle,OUTPUT);
}

void gas(boolean power){
  digitalWrite(pin_gas_handdle,power);
}



