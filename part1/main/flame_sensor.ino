int pin_flame_sensor1 = 5;
int pin_flame_sensor2 = 4;
int pin_flame_sensor3 = 3;

void flame_sensor_setup(){
  pinMode(pin_flame_sensor1,INPUT);
  pinMode(pin_flame_sensor2,INPUT);
  pinMode(pin_flame_sensor3,INPUT);
}

int flame_sensor1(){
  int value = digitalRead(pin_flame_sensor1);
  return value;
}
int flame_sensor2(){
  int value = digitalRead(pin_flame_sensor2);
  return value;
}
int flame_sensor3(){
  int value = digitalRead(pin_flame_sensor3);
  return value;
}

