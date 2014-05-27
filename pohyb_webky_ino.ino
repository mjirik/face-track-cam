#include <Servo.h>
Servo myServoH;
Servo myServoV;

const int horizontal_servo = 6;
const int vertical_servo = 7;
int krok = 5;
int poloha_vertical = 70;
int poloha_horizontal = 70;
int aktual_vertical = 90;
int aktual_horizontal = 90;
boolean pokracuj = false;
String zprava = "";

void setup(){
  Serial.begin(57600);
  myServoH.attach(horizontal_servo);
  myServoV.attach(vertical_servo);
}
void pohyb(){
  while(pokracuj){
    myServoH.write(poloha_horizontal);
    myServoV.write(poloha_vertical);
    aktual_horizontal = myServoH.read();
    aktual_vertical = myServoV.read();
   if((aktual_vertical == poloha_vertical)&&(aktual_horizontal == poloha_horizontal)){
    Serial.println(pokracuj);
    pokracuj = false;
  }  
 } 
}
void loop(){
while (Serial.available()==0);
 {
   char znak=Serial.read();
   if ((znak!='h')||(znak!='v'))
   {
     zprava=zprava+znak;
   }    
   if (znak=='h')
   {
     poloha_horizontal=(float)zprava.toInt();
     zprava="";
     pokracuj=false;;
   }
   if (znak=='v')
   {
     poloha_vertical=(float)zprava.toInt();
     zprava="";
     pokracuj=true;;
   }
   pohyb();
 }  
}
