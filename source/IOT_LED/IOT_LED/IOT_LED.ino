#include <WiFi.h>

const char *ssid = "ANE_Class2_2G";
const char *password = "addinedu_class2@";

WiFiServer server(80);



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("ESP32 TCP Server Start");
  Serial.println(ssid);


  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("IP Address : ");
  Serial.println(WiFi.localIP());

  server.begin();

}


void loop() {
  // put your main code here, to run repeatedly:
  WiFiClient client = server.available();
  if(client){
    Serial.print("Client Connected : ");
    Serial.println(client.remoteIP());
   
    while (client.connected()){
      while (client.available()>0){
        char c = client.read();
        Serial.print(c);
        
      }
      delay(10);
    }

    client.stop();
    Serial.println("Client Disconnected!");

  }

}
