int pin_gas_sensor = A0;

int gas_sensor(){
  float sensor_volt = analogRead(pin_gas_sensor)*5.0/1024;
  float RS_gas = (5.0-sensor_volt)/sensor_volt;
  float ratio = RS_gas/3.0; 
  return ratio;
}
