void led_color_value(String led_value) {
//  Serial.print("value: ");
//  Serial.println(led_value);
  led_value.remove(0, 1);

  led_value = String(led_value.toInt(), HEX);
  if (led_value.length() < 6)
  {
    switch (led_value.length())
    {
      case 0:
        led_value = "000000";
        break;
      case 1:
        led_value = "00000" + led_value;
        break;
      case 2:
        led_value = "0000" + led_value;
        break;
      case 3:
        led_value = "000" + led_value;
        break;
      case 4:
        led_value = "00" + led_value;
        break;
      case 5:
        led_value = "0" + led_value;
        break;
    }
  }
  String color = String(led_value[0]) + String(led_value[1]);

  for (int i = 0; i < 3; i++)
  {
    led_color[i] = StringToNum(led_value[i * 2], led_value[i * 2 + 1]);
  }
  /*for (int i = 0; i < 3; i++)
  {
    Serial.println(led_color[i]);
  }
*/
}

int StringToNum(char a, char b)
{
  int resualt;
  resualt = HextoDec(a) * 16 + HextoDec(b);

  return resualt;
}

int HextoDec(char num)
{
  int resualt;
  switch (num)
  {
    case '0':
      resualt = 0;
      break;
    case '1':
      resualt = 1;
      break;
    case '2':
      resualt = 2;
      break;
    case '3':
      resualt = 3;
      break;
    case '4':
      resualt = 4;
      break;
    case '5':
      resualt = 5;
      break;
    case '6':
      resualt = 6;
      break;
    case '7':
      resualt = 7;
      break;
    case '8':
      resualt = 8;
      break;
    case '9':
      resualt = 9;
      break;
    case 'a':
      resualt = 10;
      break;
    case 'b':
      resualt = 11;
      break;
    case 'c':
      resualt = 12;
      break;
    case 'd':
      resualt = 13;
      break;
    case 'e':
      resualt = 14;
      break;
    case 'f':
      resualt = 15;
      break;
  }

  return resualt;
}
