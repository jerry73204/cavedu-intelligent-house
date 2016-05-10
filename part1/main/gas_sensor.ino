int pin_gas_sensor = A0;

int gas_sensor(){
  int value = analogRead(pin_gas_sensor);
  return value;
}
