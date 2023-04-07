// #include < Wire .h> we are removing this because it is already added in liquid crystal library
#include <LiquidCrystal_I2C.h>
#include <ThreeWire.h>  
#include <RtcDS1302.h>
 
int led_R = 19;
int led_G = 18;
int led_B = 17;

// Create the lcd object address 0x3F and 16 columns x 2 rows 
LiquidCrystal_I2C lcd (0x27, 16,2);  // lcd SDA : 21, SCL : 22
ThreeWire myWire(26,27,14); // DAT : 26, CLK : 27, RST : 14
RtcDS1302<ThreeWire> Rtc(myWire);
 
void  setup () {
  
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
  
}
 
void loop() {


  //시간 표시
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

  // 감정 표시
  lcd.setCursor(0,1);
  lcd.print("emotion:");
  lcd.print("u seok");

}
