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
