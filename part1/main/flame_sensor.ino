/*
 * Copyright (C) HENNES CO., LTD. - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written in May 2016 by
 * Li-Wei Shih
 * Hao-Yun Hsueh
 * Feng-Chih Hsu
 * Hsiang-Jiu Lin
 * Cheng-Chang Liu
 * Pei-Hsuan Yan
 */
int pin_flame_sensor = 5;

void flame_sensor_setup(){
  pinMode(pin_flame_sensor,INPUT);
}

int flame_sensor(){
  int value = 1 - digitalRead(pin_flame_sensor);
  return value;
}
