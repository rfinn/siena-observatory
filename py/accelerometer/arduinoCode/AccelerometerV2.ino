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

int keyIndex = 0;            // your network key Index number (needed only for WEP)

int status = WL_IDLE_STATUS;
WiFiServer server(23);

unsigned int localPort = 23;

char packetBuffer[255]; //buffer to hold incoming packet
char ReplyBuffer[] = "acknowledged"; // a string to send back

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

  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remoteIp = Udp.remoteIP();
    Serial.print(remoteIp);
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) packetBuffer[len] = 0;
    Serial.println("Contents:");
    Serial.println(packetBuffer);

    // send a reply, to the IP address and port that sent us the packet we received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(ReplyBuffer);
    Udp.endPacket();
   }

   // read accelerometer
   mma.read();
   
   // send a reply, to the IP address and port that sent us the packet we received
   Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    
   // create a string of x,y,z acceleration?
   // or send each one separately
   Udp.write('N'); // signal new acceleration measurement
   Udp.endPacket();


   /*
    * might be easier to send raw counts because we know they are 14 bits - 
    * one bit for +/-, and 2**13 bits for number (2**13 = 8192).
    * 
    * The range of values is -8192 to 8192 and spans the range of +/- 2G, 4G, 8G.
    * If we use the 2G setting, then 2.*9.8/8192 means 0.0023925 per bit
    * or
    * ax(m/s^2) = mma.x*.0023925
    * 
    * This might be faster because the conversion between bits and m/s^2 
    * could be done by the plotting program and not by the arduino or reading program.
    * 
    * so how do we specify the buffer size for a 14-bit value?
    * 8 bits per byte, so 14 bits = 1.75 bytes
    * 
    * is it ok to send partial bytes??
    * 
    * info on the udp library is here
    * https://www.arduino.cc/en/Reference/WiFi101
     */
   Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
   Udp.print(mma.x);
   Udp.endPacket();
   Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
   Udp.print(mma.y);
   Udp.endPacket();
   Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
   Udp.print(mma.z);
   Udp.endPacket();
   //Serial.println(mma.x);
   //Serial.println(mma.y);
   //Serial.println(mma.z);
   

   //Udp.write(mma.y, 1.75);
   //Udp.write(mma.z, 1.75);
   
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


