void mcs(char s,int geo){
  Serial1.print(s);
  Serial1.print('g');
  Serial1.print(gas_sensor());
  Serial1.print('f');
  Serial1.print(flame_sensor1());
  Serial1.print('e');
  Serial1.print(geo);
  Serial1.println('o');
}
