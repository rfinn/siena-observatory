/*
 Chat  Server

 A simple server that distributes any incoming messages to all
 connected clients.  To use telnet to  your device's IP address and type.
 You can see the client's input in the serial monitor as well.

 This example is written for a network using WPA encryption. For
 WEP or WPA, change the WiFi.begin() call accordingly.


 Circuit:
 * WiFi shield attached

 created 18 Dec 2009
 by David A. Mellis
 modified 31 May 2012
 by Tom Igoe

 */

#include <SPI.h>
#include <WiFi101.h>

#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();

char ssid[] = "SOS_Wireless"; //  your network SSID (name)
char pass[] = "secretPassword";    // your network password (use for WPA, or use as key for WEP)

int keyIndex = 0;            // your network key Index number (needed only for WEP)

int status = WL_IDLE_STATUS;
int i = 0;
WiFiServer server(23);

boolean alreadyConnected = false; // whether or not the client was connected previously



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
    status = WiFi.begin(ssid);

    // wait 10 seconds for connection:
    delay(10000);
  // initialize accelerometer
    
  Serial.println("Adafruit MMA8451 test!");
  

  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("MMA8451 found!");
  
  mma.setRange(MMA8451_RANGE_2_G);
  
  Serial.print("Range = "); Serial.print(2 << mma.getRange());  
  Serial.println("G");
  }

  // start the server:
  server.begin();
  // you're connected now, so print out the status:
  printWiFiStatus();
}


void loop() {

  // wait for a new client:
  WiFiClient client = server.available();


  // when the client sends the first byte, say hello:
  if (client) {
    if (!alreadyConnected) {
      // clead out the input buffer:
      client.flush();
      Serial.println("We have a new client");
      client.println("Hello, client!");
      alreadyConnected = true;
    }
    if (i < 10) {
    //if (client.available() > 0) {
      // Read the 'raw' data in 14-bit counts
      mma.read();
      Serial.println(mma.x);
      client.println(mma.x); 
      //Serial.print("\tY:\t"); Serial.print(mma.y); 
      //Serial.print("\tZ:\t"); Serial.print(mma.z); 
      //Serial.println();
  
      /* Get a new sensor event */ 
      //sensors_event_t event; 
      //mma.getEvent(&event);

      /* Display the results (acceleration is measured in m/s^2) */
      //Serial.print("X: \t"); Serial.print(event.acceleration.x); Serial.print("\t");
      //Serial.print("Y: \t"); Serial.print(event.acceleration.y); Serial.print("\t");
      //Serial.print("Z: \t"); Serial.print(event.acceleration.z); Serial.print("\t");
      //Serial.println("m/s^2 ");
      
//      // read the bytes incoming from the client:
//      char thisChar = client.read();
//      // echo the bytes back to the client:
//      server.write(thisChar);
//      // echo the bytes to the server as well:
//      Serial.write(thisChar);
    }
    i += 1;
  }
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


