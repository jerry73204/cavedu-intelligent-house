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
