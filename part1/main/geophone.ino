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
int pin_geophone = A1;

int geophone(){
  int seismic = 0;
  float volt = 0;
  float pvolt = 0;
  int deltaT = 4;
  float accel = 0;
  float sum = 0;
  int count = 50;
  volt = analogRead(A1)/32;
  volt = volt/32.0*5;
  delay(deltaT);
  for(int i = 0;i < count;i++){
    pvolt = volt;
    volt = analogRead(A1)/32;
    volt = volt/32.0*5;
    delay(deltaT);
    sum += abs(volt - pvolt);
  }
  accel = sum/deltaT/count*1000/0.288;
  if(accel < 0.8){
    seismic = 0;
  }
  else if(accel < 0.8){
    seismic = 0;
  }
  else if(accel < 2.5){
    seismic = 1;
  }
  else if(accel < 8){
    seismic = 2;
  }
  else if(accel < 25){
    seismic = 3;
  }
  else if(accel < 80){
    seismic = 4;
  }
  else if(accel < 250){
    seismic = 5;
  }
  else if(accel < 400){
    seismic = 6;
  }
  else{
    seismic = 7;
  }
  return seismic;
}
