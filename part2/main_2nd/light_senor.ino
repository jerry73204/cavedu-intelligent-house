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
int LightSensor()
{
  int value = analogRead(pinLight);
  value = map(value, 0, 1023, 0, 100);
  return value;
}
int Solar()
{
  int value = analogRead(A5);
  if (value > 255)
    value = 1;
  else
    value = 0;

  return value;

}
