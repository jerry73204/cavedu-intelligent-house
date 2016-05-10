boolean LastRoomBtnStatus, LastCurBtn;

boolean CRB = false;
boolean CCB = true;

void RoomBtn()
{
  boolean Btn = digitalRead(A2);

  if (Btn != LastRoomBtnStatus)
  {
    if (Btn)
    {
      CRB = !CRB;

      if (livlight)
      {
        Serial.println("livingroom light off");
        colorWipe_living(strip_living.Color(0, 0, 0), 0);
        livlight = false;
      }
      else
      {
        Serial.println("livingroom light on!");
        colorWipe_living(strip_living.Color(led_color[0], led_color[1], led_color[2]), 0);
        livlight = true;
      }
      delay(50);
    }
  }
  LastRoomBtnStatus = Btn;

}

int Curtain()
{
  int x = map(analogRead(A3), 0, 1023, 0, 100);
  if (x < 10)
    x = 0;
  if (x > 90)
    x = 100;
  return x;
}

void AutoCurtain()
{
  boolean Btn = digitalRead(A4);

  if (Btn != LastCurBtn)
  {
    if (Btn)
    {
      CCB = !CCB;
      digitalWrite(13, CCB);
      if (CCB)
        Serial.println("Auto Curtain");
      else
      {
        Serial.println("manual Curtain");
        stepper_move(Curtain());
      }
      delay(50);

    }
  }
  if (!CCB)
    stepper_move(Curtain());
  LastCurBtn = Btn;
}

void move_curtain()
{

  int s = Curtain();
  stepper_move(s);

}

