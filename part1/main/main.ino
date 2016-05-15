int geo = 0;
float gas_value = 0;
int count = 0;
float R0 = 2.5;
void setup() {
  Serial.begin(9600);
  Serial1.begin(57600);
  serial_setup();
  handdle_setup();
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
    count++;
    if(count == 30){
      mcs('s',geo,gas_value);
      count = 0;
    }
  }
  
  //----------earthquake----------
  else if(Status == 1){
    Serial.println("earthquake strikes");
    //----------send message----------
    sendText(1,'E');//Linkit One Text
    sendText(2,'E');//Light
    sendText(3,'E');//Door
    mcs('E',geo,gas_value);
    door(true);
    delay(1000);
    //----------warring----------
    buzzE();
    //----------safe----------
    Serial.println("silmulation over");
    door(false);
    sendText(1,'S');
    sendText(2,'S');
    sendText(3,'S');
    delay(1000);
  }
  
  //----------fire----------
  else if(Status == 2){
    Serial.println("house is on fire");
    
    //----------send message----------
    sendText(1,'F');//Linkit One Text
    sendText(2,'F');//Light
    sendText(3,'F');//Door
    mcs('F',geo,gas_value);
    door(true);
    delay(1000);
    //----------warring----------
    buzzF();
    //----------safe----------
    Serial.println("silmulation over");
    door(false);
    sendText(1,'S');
    sendText(2,'S');
    sendText(3,'S');
    delay(1000);
  }
  
  //----------gas leak----------
  else if(Status == 3){
    Serial.println("gas is leaking");
    //----------handdle----------
    gas(true);
    delay(1000);
    //----------send message----------
    sendText(1,'G');
    mcs('G',geo,gas_value);
    //----------warning----------
    buzzG();
    //----------safe----------
    Serial.println("silmulation over");
    gas(false);
    sendText(1,'S');
    delay(1000);
  }
  
  //----------door not close----------
  else if(Status == 4){
    Serial.println("door is not closed");
    delay(1000);
    buzzD();
    //----------send message----------
    sendText(1,'D');
    mcs('D',geo,gas_value);
    Serial.println("massage has been sent");
    delay(1000);
  }
  
  //----------house is invaded----------
  else if(Status == 5){
    Serial.println("some enter into the house");
    delay(1000);
    buzzI();
    //----------send message----------
    sendText(1,'I');
    mcs('I',geo,gas_value);
    Serial.println("massage has been sent");
    delay(1000);
  }
  
  //----------sensor value----------
  Serial.println("-------------------");
  Serial.print("gas sensor:  ");
  Serial.println(gas_value);
  Serial.print("flame sensor:  ");
  Serial.println(flame_sensor());
  Serial.print("earthquake sensor:  ");
  Serial.println(geo);
}

int checkCondition(){
  geo = geophone();
  gas_value = gas_sensor(R0);
  char readMsg = readText(); //get message
  //check condition
  
  int result = 0;
  //----------earthquake----------
  if(readMsg == 'E'){
    result = 1;
  }
  //----------fire----------
  else if(readMsg == 'F'){
    result = 2;
  }
  //----------gas leak----------
  else if(readMsg == 'G'){
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
  return result;
}
