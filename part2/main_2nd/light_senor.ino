int LightSensor()
{
  int value = analogRead(pinLight);
  value = map(value,0,1023,0,100);
  return value;
}
