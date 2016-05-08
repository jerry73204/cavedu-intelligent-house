int pin_flame_sensor1 = 5;

void flame_sensor_setup(){
  pinMode(pin_flame_sensor1,INPUT);
}

int flame_sensor1(){
  int value = digitalRead(pin_flame_sensor1);
  return value;
}
