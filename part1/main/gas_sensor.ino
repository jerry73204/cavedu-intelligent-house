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
int pin_gas_sensor = A0;

float gas_sensor(float R0){
  float sensor_volt = analogRead(pin_gas_sensor)*5/1024.0;
  float RS_gas = (5.0-sensor_volt)/sensor_volt;
  float ratio = RS_gas/R0;
  return ratio;
}
