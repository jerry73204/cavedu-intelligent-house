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
