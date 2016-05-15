int pin_flame_sensor = 5;

void flame_sensor_setup(){
  pinMode(pin_flame_sensor,INPUT);
}

int flame_sensor(){
  int value = 1 - digitalRead(pin_flame_sensor);
  return value;
}
