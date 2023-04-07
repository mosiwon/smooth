#include <WiFi.h>
#include <LiquidCrystal_I2C.h>
#include <ThreeWire.h>  
#include <RtcDS1302.h>

const char *ssid = "siwonhotspot";
const char *password = "00001234";
int led_R = 19;
int led_G = 18;
int led_B = 17;
int current_R = 0;
int current_G = 0;
int current_B = 0;
int current_emotion = 8;
// emotion 변수 문자열 선언 
char Anger_emotion_str[] = "Anger";
char Contempt_emotion_str[] = "Contempt";
char Disgust_emotion_str[] = "Disgust";
char Fear_emotion_str[] = "Fear";
char Happiness_emotion_str[] = "Happiness";
char Neutral_emotion_str[] = "Neutral";
char Sadness_emotion_str[] = "Sadness";
char Surprise_emotion_str[] = "Surprise";


WiFiServer server(80);
// Create the lcd object address 0x3F and 16 columns x 2 rows 
LiquidCrystal_I2C lcd (0x27, 16,2);  // lcd SDA : 21, SCL : 22
ThreeWire myWire(26,27,14); // DAT : 26, CLK : 27, RST : 14
RtcDS1302<ThreeWire> Rtc(myWire);

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
  Rtc.Begin();
  RtcDateTime now = Rtc.GetDateTime();

  // Initialize the LCD connected 
  lcd. begin ();
  // Turn on the backlight on LCD. 
  lcd. backlight ();
  Serial.begin(115200);
  pinMode(led_R,OUTPUT);
  pinMode(led_G,OUTPUT);
  pinMode(led_B,OUTPUT);

  server.begin();
}


void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.print("Client Connected : ");
    Serial.println(client.remoteIP());

    while (client.connected()) {
      if (client.available() >= 4 * sizeof(uint8_t)) { // RGB 각각 1바이트씩 읽음
        uint8_t data[4];
        client.readBytes(data, sizeof(data));

        uint8_t r, g, b, emotion;
        memcpy(&r, data, sizeof(uint8_t));
        memcpy(&g, data + 1, sizeof(uint8_t));
        memcpy(&b, data + 2, sizeof(uint8_t));
        memcpy(&emotion, data + 3, sizeof(uint8_t));

        if (r != current_R || g != current_G || b != current_B || emotion !=current_emotion) {

          // 최대 증가 스텝 계산
          int steps = max(max(abs(r - current_R), abs(g - current_G)), abs(b - current_B));

          // 단일 for 루프로 RGB 값 천천히 변경
          for (int step = 0; step < steps; step++) {
            if (r != current_R) {
              current_R += (r - current_R) / abs(r - current_R);
              analogWrite(led_R, current_R);
            }
            if (g != current_G) {
              current_G += (g - current_G) / abs(g - current_G);
              analogWrite(led_G, current_G);
            }
            if (b != current_B) {
              current_B += (b - current_B) / abs(b - current_B);
              analogWrite(led_B, current_B);
            }
            delay(10);
          }
          
          if (emotion == 0)
          {
              lcd.setCursor(0,1);
              lcd.print("emotion:");
              lcd.print(Anger_emotion_str);
              lcd.print("       ");
          }
          else if (emotion == 1)
          {
              lcd.setCursor(0,1);
              lcd.print("emotion:");
              lcd.print(Contempt_emotion_str);
              lcd.print("       ");
          }
          else if (emotion == 2)
          {
              lcd.setCursor(0,1);
              lcd.print("emotion:");
              lcd.print(Disgust_emotion_str);
              lcd.print("       ");
          }
          else if (emotion == 3)
          {
              lcd.setCursor(0,1);
              lcd.print("emotion:");
              lcd.print(Fear_emotion_str);
              lcd.print("       ");
          }
          else if (emotion == 4)
          {
              lcd.setCursor(0,1);
              lcd.print("emotion:");
              lcd.print(Happiness_emotion_str);
              lcd.print("       ");
          }
          else if (emotion == 5)
          {
              lcd.setCursor(0,1);
              lcd.print("emotion:");
              lcd.print(Neutral_emotion_str);
              lcd.print("       ");
          }
          else if (emotion == 6)
          {
              lcd.setCursor(0,1);
              lcd.print("emotion:");
              lcd.print(Sadness_emotion_str);
              lcd.print("       ");
          }
          else if (emotion == 7)
          {
              lcd.setCursor(0,1);
              lcd.print("emotion:");
              lcd.print(Surprise_emotion_str);
              lcd.print("       ");
          }

          current_emotion = emotion;
        }
      }
      RtcDateTime now = Rtc.GetDateTime();
      // Print the date on the LCD
      lcd.setCursor(0, 0); // Set cursor to the first column of the first row
      lcd.print(now.Month(), DEC);
      lcd.print('/');
      lcd.print(now.Day(), DEC);
      // Print the time on the LCD
      lcd.print("  ");
      lcd.print(now.Hour(), DEC);
      lcd.print(':');
      lcd.print(now.Minute(), DEC);
      lcd.print(':');
      lcd.print(now.Second(), DEC);      
      delay(10);
    }
    client.stop();
    Serial.println("Client Disconnected!");
  }
}