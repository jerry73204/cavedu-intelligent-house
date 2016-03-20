int pin_emg = 1;

void led_emg_setup(){
  pinMode(pin_emg,OUTPUT);
}

void led_emg(boolean power){
  digitalWrite(pin_emg,power);
}
