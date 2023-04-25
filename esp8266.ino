#include <Arduino.h>
#include "MHZ19.h"                                        
#include <SoftwareSerial.h>                                
#include <DFRobot_DHT11.h>
DFRobot_DHT11 DHT;
#define DHT11_PIN 16

#include "PMS.h"  

#include "AGS02MA.h"
AGS02MA AGS(26);                                    

#define RX_PIN 13 //for MHZ19 sensor
#define TX_PIN 15 //for MHZ19 sensor
#define BAUDRATE 9600 // for MHZ29 sensor

MHZ19 myMHZ19;                                             
SoftwareSerial mySerial(RX_PIN, TX_PIN);                   
unsigned long getDataTimer = 0;
int pm25;
int co2;
int hum;
int tmp;
int a=0;
String buff="@";
String out="";
SoftwareSerial pmsSerial(12, 14); //GPIO pins where the Rx and Tx pins of PMS 7003 sensor is connected
PMS pms(pmsSerial);
PMS::DATA data;
void setup()
{
    Serial.begin(9600);                                     
    pmsSerial.begin(9600);
    mySerial.begin(BAUDRATE);                               
    myMHZ19.begin(mySerial);                                

    myMHZ19.autoCalibration();                              
    bool b = AGS.begin();
    b = AGS.setPPBMode();
}

void loop()
{
             
    co2 = myMHZ19.getCO2();                                                            
    uint32_t value = AGS.readPPB();
    
    a = analogRead(A0);
    DHT.read(DHT11_PIN);
    hum=DHT.humidity;
    tmp=DHT.temperature;
    
    pmsSerial.listen();
    pms.readUntil(data);
    pm25 = data.PM_AE_UG_1_0;

    out= String(co2)+buff+String(hum)+buff+String(pm25)+buff+String(tmp)+buff+String(value)+buff+String(a);
    Serial.println(out);
    delay(1);

    
}
