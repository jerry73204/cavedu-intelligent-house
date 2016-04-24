void setup() {
  Serial.begin(9600);
  Serial1.begin(57600);
  serial_setup();
  led_emg_setup();
  gas_led_setup();
  fan_setup();
  flame_sensor_setup();
}

void loop() {
  Serial.println("-------------------");
  //----------check condition----------
  int Status = checkCondition();//0-normal,1-fire,2-earthquake,3-gas,4-door,5-invasion
  
  //----------nothing happened----------
  if(Status == 0){
    Serial.println("nothing happened");
    mcs('s');
    delay(1000);
  }
  
  //----------earthquake----------
  else if(Status == 1){
    Serial.println("earthquake strikes");
    
    //----------warring----------
    buzz(true);
    warring_light(true);
    LCD("an earthquake of magnitude" + (String)geophone() + "strikes");
    delay(1000);
    Serial.println("warring!");
    delay(1000);
    
    //----------emergency light----------
    led_emg(true);
    Serial.println("turn on emergency light");
    delay(1000);
    
    //----------send message----------
    sendText(1,'E');//Linkit One Text
    sendText(2,'E');//Light
    sendText(3,'E');//Door
    mcs('E');
    Serial.println("massage has been sent");
    delay(1000);
    
    //----------safe----------
    Serial.println("silmulation over");
    sendText(2,'S');
    sendText(3,'S');
    delay(1000);
  }
  
  //----------fire----------
  else if(Status == 2){
    Serial.println("house is on fire");
    delay(1000);
    
    //----------warring----------
    buzz(true);
    warring_light(true);
    LCD("fire is detected in kitchen");
    Serial.println("warring!");
    delay(1000);
    
    //----------emergency light----------
    led_emg(true);
    Serial.println("turn on emergency light");
    delay(1000);
    
    //----------send message----------
    sendText(1,'F');//Linkit One Text
    sendText(2,'F');//Light
    sendText(3,'F');//Door
    mcs('F');
    Serial.println("massage has been sent");
    delay(1000);
    
    //----------safe----------
    Serial.println("silmulation over");
    sendText(2,'S');
    sendText(3,'S');
    delay(1000);
  }
  
  //----------gas leak----------
  else if(Status == 3){
    Serial.println("gas is leaking");
    delay(1000);
    
    warring_light(true);
    Serial.println("warring!");
    delay(1000);
    
    gas_interruption(true);
    Serial.println("gas_interruption");
    delay(1000);
    
    fan(true);
    Serial.println("turn on fan");
    delay(1000);
    //----------send message----------
    sendText(1,'G');
    mcs('G');
    Serial.println("massage has been sent");
    
    delay(1000);
    Serial.println("silmulation over");
  }
  
  //----------door not close----------
  else if(Status == 4){
    Serial.println("door is not closed");
    delay(1000);
    
    //----------send message----------
    sendText(1,'D');
    mcs('D');
    Serial.println("massage has been sent");
    delay(1000);
  }
  
  //----------house is invaded----------
  else if(Status == 5){
    Serial.println("some enter into the house");
    delay(1000);
    
    //----------send message----------
    sendText(1,'I');
    mcs('I');
    Serial.println("massage has been sent");
    delay(1000);
  }
  
  //----------sensor value----------
  Serial.println("-------------------");
  Serial.print("gas sensor:  ");
  Serial.println(gas_sensor());
  Serial.print("flame sensor in kicten:  ");
  Serial.println(flame_sensor1());
  Serial.print("flame sensor in dining room:  ");
  Serial.println(flame_sensor2());
  Serial.print("flame sensor in aisle:  ");
  Serial.println(flame_sensor3());
  Serial.print("geophone:  ");
  Serial.println(geophone());
  
}

int checkCondition(){
  //----------get message----------
  char readMsg = readText();
  //----------check condition----------
  int result = 0;
  //----------earthquake----------
  if(readMsg == 'E' || geophone() > 200){
    result = 1;
  }
  //----------fire----------
  else if(readMsg == 'F' || flame_sensor1() == 1){
    result = 2;
  }
  //----------gas leak----------
  else if(readMsg == 'G' || gas_sensor() > 100){
    result = 3;
  }
  //----------door not closed----------
  else if(readMsg == 'D'){
    result = 4;
  }
  //----------house is invaded----------
  else if(readMsg == 'I'){
    result = 5;
  }
  //----------nothing happened----------
  else{
    result = 0;
  }
  Serial.println(result);
  return result;
}
