#include <Adafruit_NeoPixel.h>
#include <DHT.h>
#include <FlexiTimer2.h>
#include <SoftwareSerial.h>
#include <Stepper.h>

/////define pin/////

#define DHTPIN1 4 //outside
#define DHTPIN2 8 //inside
#define DHTTYPE DHT11

#define PIN 3
#define PIN_living 6
#define PIN_escape 9
#define STRIPSIZE 10
#define STRIPSIZELIV 64
#define STRIPSIZEESCAPE 24
#define STEPS 2048

Stepper stepper(STEPS, 2, 5, 7, 12);

Adafruit_NeoPixel strip = Adafruit_NeoPixel(STRIPSIZE, PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_living = Adafruit_NeoPixel(STRIPSIZELIV, PIN_living, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_escape = Adafruit_NeoPixel(STRIPSIZEESCAPE, PIN_escape, NEO_GRB + NEO_KHZ800);

DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

SoftwareSerial linkit7688(10, 11);

int led_color[3] = {255, 255, 255};
const int pinLight = A0;
boolean danger = false;
String sensor_value[9] = {"l", "", "i", "", "p", "", "s", "", "e"};
int temp_1, temp_2;
boolean livlight, roomlight;

int current_step = 1;
int unit_step = 10;

void flash() {

  sensor_value[1] = String(LightSensor());
  sensor_value[3] = String(temp_1);
  sensor_value[5] = String(temp_2);
  sensor_value[7] = String(Solar());
  for (int i = 0; i < 9; i++)
  {
    Serial1.print(sensor_value[i]);
    //Serial.println(sensor_value[i]);
    //delay(50);
  }
  //Serial.println("");
  Serial1.println("");
}

void setup() {

  /////Serial init//////

  Serial.begin(9600);
  Serial1.begin(57600);
  linkit7688.begin(9600);

  delay(5);
  Serial1.println("R");
  stepper.setSpeed(5);
  //////init led///////

  strip.begin();
  strip.setBrightness(25);
  strip.show();

  strip_living.begin();
  strip_living.setBrightness(25);
  strip_living.show();

  strip_escape.begin();
  strip_escape.setBrightness(25);
  strip_escape.show();

  dht1.begin();
  dht2.begin();
  while (current_step != 0)
    step_reset();
  FlexiTimer2::set(5000, flash);
  FlexiTimer2::start();
}

void loop() {

  String read_meg = "";

  if (linkit7688.available() || danger)
  {

    while (linkit7688.available())
    {
      read_meg = read_meg + char(linkit7688.read());
      Serial.println(read_meg);
    }
    if (read_meg.equals("S"))
    {
      Serial.println("Safe!");
      Safe();
      danger = false;
      Serial1.println("S");
      colorWipe_escape(strip_escape.Color(0, 0, 0), 0);
      colorWipe(strip.Color(0, 0, 0), 0);
      FlexiTimer2::start();
    }
    else if (read_meg.equals("E") || read_meg.equals("F") || danger )
    {
      Serial.println("danger!");
      danger = true;
      Serial1.println("D");
      AllStop();
      colorWipe(strip.Color(255, 255, 255), 0);
      delay(50);
      colorWipe_escape(strip_escape.Color(255, 255, 255), 200);
      colorWipe_escape(strip_escape.Color(0, 0, 0), 200);
      FlexiTimer2::stop();
    }

  }
  if (!danger) {
    if (Serial1.available())
    {
      while (Serial1.available())
        read_meg = read_meg + char(Serial1.read());

      read_meg.trim();

      Serial.println(read_meg);
      Serial.println(read_meg.length());

      //////////////AUTO / MANUAL//////////////////

      if (read_meg.equals("au"))
      {
        Serial.println("system auto");
      }
      else if (read_meg.equals("ma"))
      {
        Serial.println("manual");
      }
      ///////////////room light////////////////////
      /*
            if (read_meg.equals("ro"))
            {
              Serial.println("room light on!");
              colorWipe(strip.Color(255, 255, 255), 0);
              roomlight = true;
            }

            else if (read_meg.equals("rc"))
            {
              Serial.println("room light off");
              colorWipe(strip.Color(0, 0, 0), 0);
              roomlight = false;
            }
      */
      ///////////////living room/////////////////

      if (read_meg.equals("lo"))
      {
        Serial.println("livingroom light on!");
        colorWipe_living(strip_living.Color(led_color[0], led_color[1], led_color[2]), 0);
        livlight = true;
      }
      else if (read_meg.equals("lc"))
      {
        Serial.println("livingroom light off");
        colorWipe_living(strip_living.Color(0, 0, 0), 0);
        livlight = false;
      }

      //////////////living color//////////////////
      if (read_meg[0] == 'c')
      {

        if (read_meg.length() > 1)
        {
          Serial.println("change color!");
          led_color_value(read_meg);
          if (livlight)
            colorWipe_living(strip_living.Color(led_color[0], led_color[1], led_color[2]), 0);

        }
      }//if (read_meg[0] == 'c')

    }//if (Serial1.available())

    //////////////////Curtain///////////////

    AutoCurtain();

    ///////////manual living room light///////////
    RoomBtn();

  }//if(!danger)
  temp_1 = TempSensor(4);
  temp_2 = TempSensor(8);


}//loop
