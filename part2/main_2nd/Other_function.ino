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
void AllStop()
{
  colorWipe_living(strip_living.Color(0, 0, 0), 0);

}

void Safe()
{
  if (livlight)
    colorWipe_living(strip_living.Color(led_color[0], led_color[1], led_color[2]), 0);
}
