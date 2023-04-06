#include <WiFi.h>

const char *ssid = "ANE_Class2_2G";
const char *password = "addinedu_class2@";

WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 TCP Server Start");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("IP Address : ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.print("Client Connected : ");
    Serial.println(client.remoteIP());

    while (client.connected()) {
      while (client.available() >= 12) { // 12바이트(R128G128B128)씩 읽음
        char color_str[16];  // 최대 3자리 * 3 (R, G, B) + NULL 문자
        client.readBytesUntil('G', color_str, 4);  // R값 읽기
        uint8_t r = atoi(color_str + 1);  // "R" 제외한 부분 파싱
        client.readBytesUntil('B', color_str, 4);  // G값 읽기
        uint8_t g = atoi(color_str + 1);  // "G" 제외한 부분 파싱
        client.readBytesUntil('\r', color_str, 4);  // B값 읽기
        uint8_t b = atoi(color_str + 1);  // "B" 제외한 부분 파싱
        sprintf(color_str, "R%dG%dB%d", r, g, b);  // 문자열로 변환
        Serial.println(color_str);
        // 받은 RGB 값을 이용하여 LED 켜기 등의 작업 수행
      }
      delay(10);
    }

    client.stop();
    Serial.println("Client Disconnected!");
  }
}
