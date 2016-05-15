void mcs(char s,int geo,float gas_value){
  Serial1.print(s);
  Serial1.print(",");
  Serial1.print(gas_value);
  Serial1.print(",");
  Serial1.print(flame_sensor());
  Serial1.print(",");
  Serial1.print(geo);
}
