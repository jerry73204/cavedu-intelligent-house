int pin_geophone = A0;
int gas_sensor(){
  int value = analogRead(pin_geophone);
  return value;
}
