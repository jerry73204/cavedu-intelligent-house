int LightSensor()
{
  int value = analogRead(pinLight);
  
  return value;
}
