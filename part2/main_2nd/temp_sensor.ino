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
int TempSensor(int pin)
{

  float t = 0.0;

  if (pin == 4)
  {
    t = dht1.readTemperature();
  }

  else if (pin == 8)
  {
    t = dht2.readTemperature();
  }

  return t;

}
