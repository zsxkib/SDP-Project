#include "SDPArduino.h"
#include <Wire.h>

void setup() {
//  /Serial.begin(9600);
  SDPsetup();

}

void loop() {
  if (Serial.available()>0){
    String data = Serial.readStringUntil('\n');
    if (data.equals("move_front")){
      move_front();
    }
    else if (data.equals("move_back")){
      move_back();
    }
    else if (data.equals("hatch")){
      hatch();
    }
    else if (data.equals("stop_motors")){
      stop_motors();
    }
    else {
      stop_all();
    } 
    Serial.print("You sent me: ");
    Serial.println(data);
  }
}

void move_front(){
  motorForward(0, 100);
  motorForward(1, 100);
  motorForward(2, 100);
  motorForward(3, 100);
  motorForward(4, 100);
  motorForward(5, 100);
}

void move_back(){
  motorBackward(0, 100);
  motorBackward(1, 100);
  motorBackward(2, 100);
  motorBackward(3, 100);
  motorBackward(4, 100);
  motorBackward(5, 100);
}

void hatch(){
  motorForward(3,80);
  delay(1200);
  motorBackward(3,80);
  delay(1200);
  motorStop(3);
}

void stop_motors(){
  motorStop(5);
}

void stop_all(){
  motorAllStop();
}
