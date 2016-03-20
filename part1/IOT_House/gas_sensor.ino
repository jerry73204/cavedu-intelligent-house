int gas_sensor(){
  int value = (float)analogRead(A0)/1024;
  return value;
}
