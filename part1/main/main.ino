int geo = 0;
int e_event = A2;
int f_event = A3;
int g_event = A4;
void setup() {
  Serial.begin(9600);
  Serial1.begin(57600);
  serial_setup();
  gas_setup();
  warning_setup();
  flame_sensor_setup();
}

void loop() {
  Serial.println("-------------------");
  //----------check condition----------
  int Status = checkCondition();//0-normal,1-fire,2-earthquake,3-gas,4-door,5-invasion
  
  //----------nothing happened----------
  if(Status == 0){
    Serial.println("nothing happened");
    mcs('s',geo);
    delay(5000);
  }
  
  //----------earthquake----------
  else if(Status == 1){
    Serial.println("earthquake strikes");
    
    //----------warring----------
    buzz(true);
    warring_earthquake(true);
    delay(1000);
    Serial.println("warring!");
    delay(1000);
    
    //----------send message----------
    sendText(1,'E');//Linkit One Text
    sendText(2,'E');//Light
    sendText(3,'E');//Door
    mcs('E',geo);
    Serial.println("massage has been sent");
    delay(10000);

    
    //----------safe----------
    Serial.println("silmulation over");
    buzz(false);
    warring_earthquake(false);
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
    warring_fire(true);
    Serial.println("warring!");
    delay(1000);
    
    //----------send message----------
    sendText(1,'F');//Linkit One Text
    sendText(2,'F');//Light
    sendText(3,'F');//Door
    mcs('F',geo);
    Serial.println("massage has been sent");
    delay(10000);
    
    //----------safe----------
    Serial.println("silmulation over");
    buzz(false);
    warring_fire(false);
    sendText(2,'S');
    sendText(3,'S');
    delay(1000);
  }
  
  //----------gas leak----------
  else if(Status == 3){
    Serial.println("gas is leaking");
    delay(1000);
    
    warring_gas(true);
    Serial.println("warring!");
    delay(1000);
    
    gas(true);
    Serial.println("gas_interruption");
    Serial.println("turn on fan");
    delay(1000);
    //----------send message----------
    sendText(1,'G');
    mcs('G',geo);
    Serial.println("massage has been sent");
    delay(10000);
    //----------safe----------
    Serial.println("silmulation over");
    buzz(false);
    warring_gas(false);
    gas(false);
    delay(1000);
  }
  
  //----------door not close----------
  else if(Status == 4){
    Serial.println("door is not closed");
    delay(1000);
    
    //----------send message----------
    sendText(1,'D');
    mcs('D',geo);
    Serial.println("massage has been sent");
    delay(10000);
  }
  
  //----------house is invaded----------
  else if(Status == 5){
    Serial.println("some enter into the house");
    delay(1000);
    
    //----------send message----------
    sendText(1,'I');
    mcs('I',geo);
    Serial.println("massage has been sent");
    delay(10000);
  }
  
  //----------sensor value----------
  Serial.println("-------------------");
  Serial.print("gas sensor:  ");
  Serial.println(gas_sensor());
  Serial.print("flame sensor:  ");
  Serial.println(flame_sensor1());
//  Serial.print("flame sensor in dining room:  ");
//  Serial.println(flame_sensor2());
//  Serial.print("flame sensor in aisle:  ");
//  Serial.println(flame_sensor3());
  Serial.print("earthquake sensor:  ");
  Serial.println(geo);
}

int checkCondition(){
  geo = geophone();
  //----------get message----------
  char readMsg = readText();
  //----------check condition----------
  int result = 0;
  //----------earthquake----------
  if(readMsg == 'E' || analogRead(e_event) == 1023){
    result = 1;
  }
  //----------fire----------
  else if(readMsg == 'F' || analogRead(f_event) == 1023){
    result = 2;
  }
  //----------gas leak----------
  else if(readMsg == 'G' || analogRead(g_event) == 1023){
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
