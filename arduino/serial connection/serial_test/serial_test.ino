//char dataString[50] = {0};
int a =0; 

void setup() {
Serial.begin(9600); //Starting serial communication
Serial.println(100);
}

void loop() {
  a++;                          // a value increase every loop
  //sprintf(dataString,"%02X",a); // convert a value to hexa 
  Serial.println(a);   // send the data 
  delay(1000);                  // give the loop some break
  Serial.println("shaktiman");
  loop2();
}

void loop2(){
  int s = Serial.read();
  Serial.println(s);
  delay(1000);
}
