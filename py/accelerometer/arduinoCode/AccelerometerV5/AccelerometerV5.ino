/*

This program: 
- connects to wireless network, 
- looks for a connection from an outside server
- reads acceleration data
- sends the acceleration data using UDP


Spliced together code for MMA8451 Accelerometer and WIFI101 card.

changes by R Finn:
- V2 uses udp to send data
- using Wifi101WiFiUdpSendReceiveString 

useful info on accelerometer
https://learn.adafruit.com/adafruit-mma8451-accelerometer-breakout/wiring-and-test

 */

#include <SPI.h>
// libraries for WiFi101
#include <WiFi101.h>
#include <WiFiUdp.h>
#include <Wire.h>

// libraries for accelerometer
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();

char ssid[] = "SOS_Wireless"; //  your network SSID (name)
char pass[] = "secretPassword";    // your network password (use for WPA, or use as key for WEP)
char msg[20];
int keyIndex = 0; // your network key Index number (needed only for WEP)
int nreads = 1;
//int adata[nreads];
int status = WL_IDLE_STATUS;
WiFiServer server(23);

unsigned int localPort = 23;

char packetBuffer[255]; //buffer to hold incoming packet
char ReplyBuffer[] = "acknowledged"; // a string to send back

//char accel[3];
WiFiUDP Udp;

boolean alreadyConnected = false; // whether or not the client was connected previously

int i = 0;

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }

  // attempt to connect to WiFi network:
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    //status = WiFi.begin(ssid, pass);
    status = WiFi.begin(ssid);

    // wait 10 seconds for connection:
    delay(10000);
  // initialize accelerometer
  }
  Serial.println("Connected to wifi");
  printWiFiStatus();
    
  Serial.println("Starting Adafruit MMA8451 test!");
  
  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("MMA8451 found!");
  
  mma.setRange(MMA8451_RANGE_2_G);
  
  Serial.print("Range = "); Serial.print(2 << mma.getRange());  
  Serial.println("G");
  Udp.begin(localPort);
}

void loop() {

//  // if there's data available, read a packet
//  int packetSize = Udp.parsePacket();
//  if (packetSize)
//  {
//    Serial.print("Received packet of size ");
//    Serial.println(packetSize);
//    Serial.print("From ");
//    IPAddress remoteIp = Udp.remoteIP();
//    Serial.print(remoteIp);
//    Serial.print(", port ");
//    Serial.println(Udp.remotePort());
//
//    // read the packet into packetBufffer
//    int len = Udp.read(packetBuffer, 255);
//    if (len > 0) packetBuffer[len] = 0;
//    Serial.println("Contents:");
//    Serial.println(packetBuffer);
//
//    // send a reply, to the IP address and port that sent us the packet we received
//    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
//    Udp.write(ReplyBuffer);
//    Udp.endPacket();
//   }

   // read accelerometer

//   for(count1 = 0; count1 < 50; count1++)
//   {
//   dataString += analogRead(A0);
//   dataString += ",";
//   
//   delay(10);
//   }

   //i=0;
   mma.read();
   sprintf(msg, "%d  %d  %d", mma.x,mma.y,mma.z);
   //Serial.print(msg);
   Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
   Udp.print(msg); // signal new acceleration measurement
   Udp.endPacket();
    
}


void printWiFiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}


