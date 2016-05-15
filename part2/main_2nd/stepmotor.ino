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
void stepper_move(int value)
{
  int m = (value - current_step) * unit_step;
  current_step = value;
  stepper.step(m);
  delay(20);
}

void step_reset()
{
  current_step = 1;
  int z  = digitalRead(A1);
  Serial.println(z);
  while (z != 1)
  {
    stepper.step(-10);
    z = digitalRead(A1);
    Serial.println(z);
  }

    current_step = 0;
}
