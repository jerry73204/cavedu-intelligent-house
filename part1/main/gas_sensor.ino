int pin_gas_sensor = A0;

float gas_sensor(float R0){
  float sensor_volt = analogRead(pin_gas_sensor)*5/1024.0;
  float RS_gas = (5.0-sensor_volt)/sensor_volt;
  float ratio = RS_gas/R0; 
  return ratio;
}
