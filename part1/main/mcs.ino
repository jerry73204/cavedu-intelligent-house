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
void mcs(char s,int geo,float gas_value){
  Serial1.print(s);
  Serial1.print(",");
  Serial1.print(gas_value);
  Serial1.print(",");
  Serial1.print(flame_sensor());
  Serial1.print(",");
  Serial1.print(geo);
}
