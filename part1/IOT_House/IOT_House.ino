void setup() {
  Serial.begin(9600);
  serialSetup();
  led_emg_setup();
  gas_led_setup();
  fan_setup();
}

void loop() {
  Serial.println("-------------------");
  //----------check condition----------
  int Status = checkCondition();//0-normal,1-fire,2-earthquake,3-gas,4-door,5-invasion

  //----------nothing happened----------
  if(Status == 0){
    Serial.println("nothing happened");
    MCS("geophone,",(String)geophone());
    MCS("flame_sensor,",(String)flame_sensor());
    MCS("gas_sensor,",(String)gas_sensor());

    delay(1000);
  }

  //----------earthquake----------
  else if(Status == 1){
    Serial.println("earthquake strikes");
    MCS("geophone,",(String)geophone());
    //----------warring----------
    buzz(true);
    warring_light(true);
    LCD("an earthquake of magnitude" + (String)geophone() + "strikes");
    //----------emergency light----------
    led_emg(true);
    //----------send message----------
    sendText(1,"E");//Linkit One Text
    sendText(2,"E");//Light
    sendText(3,"E");//Door
    MCS("status","earthquake");
    //----------safe----------
    Serial.println("silmulation over");
    sendText(2,"ES");
    sendText(3,"ES");

    delay(1000);
  }

  //----------fire----------
  else if(Status == 2){
    Serial.println("house is on fire");

    MCS("flame_sensor,",(String)flame_sensor());
    //----------warring----------
    buzz(true);
    warring_light(true);
    LCD("fire is detected in kitchen");
    //----------emergency light----------
    led_emg(true);
    //----------send message----------
    sendText(1,"F");//Linkit One Text
    sendText(2,"F");//Light
    sendText(3,"F");//Door
    MCS("status","fire");
    //----------safe----------
    Serial.println("silmulation over");
    sendText(2,"FS");
    sendText(3,"FS");

    delay(1000);
  }

  //----------gas leak----------
  else if(Status == 3){
    Serial.println("gas is leaking");
    MCS("gas_sensor,",(String)gas_sensor());
    warring_light(true);

    gas_interruption(true);
    fan(true);
    //----------send message----------
    sendText(1,"G");
    MCS("status","gas leak");

    delay(1000);
  }

  //----------door not close----------
  else if(Status == 4){
    Serial.println("door is not closed");
    sendText(1,"D");

    delay(1000);
  }

  //----------house is invaded----------
  else if(Status == 5){
    Serial.println("some enter into the house");
    sendText(1,"I");

    delay(1000);
  }

}

int checkCondition(){
  //----------get message----------
  String readMsg = readText();
  Serial.println(readMsg);
  //----------check condition----------
  int result = 0;
  //----------earthquake----------
  if(readMsg.equals("E")){
    result = 1;
  }
  //----------fire----------
  else if(readMsg.equals("F")){
    result = 2;
  }
  //----------gas leak----------
  else if(readMsg.equals("G")){
    result = 3;
  }
  //----------door not closed----------
  else if(readMsg.equals("D")){
    result = 4;
  }
  //----------house is invaded----------
  else if(readMsg.equals("I")){
    result = 5;
  }
  //----------nothing happened----------
  else{
    result = 0;
  }
  return result;
}
