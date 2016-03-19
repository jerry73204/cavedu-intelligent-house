void AllStop()
{
  colorWipe_living(strip_living.Color(0, 0, 0), 0);
  colorWipe(strip.Color(0, 0, 0), 0);
}

void Safe()
{
  if (roomlight)
    colorWipe(strip.Color(255, 255, 255), 0);
  if (livlight)
    colorWipe_living(strip_living.Color(led_color[0], led_color[1], led_color[2]), 0);
}
