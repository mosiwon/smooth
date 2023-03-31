#include <Arduino.h>
#include <AudioFileSourceSPIFFS.h>
#include <AudioGeneratorWAV.h>
#include <AudioOutputI2S.h>

// 전역 변수
AudioGeneratorWAV *wav;
AudioFileSourceSPIFFS *file;
AudioOutputI2S *out;

// DAC 핀 정의
const int BUILTIN_DAC_PIN = 25;

void setup() {
  Serial.begin(115200);
  delay(1000);

  // SPIFFS 초기화
  SPIFFS.begin();

  // 오디오 출력 및 파일 소스 설정
  out = new AudioOutputI2S();
  out->SetPinout(BUILTIN_DAC_PIN, -1, -1);
  file = new AudioFileSourceSPIFFS("/your_wav_file.wav");
  wav = new AudioGeneratorWAV();

  // wav 파일 재생 시작
  wav->begin(file, out);
}

void loop() {
  // 오디오 재생 중이면 계속 진행
  if (wav->isRunning()) {
    if (!wav->loop()) {
      wav->stop();
    }
  } else {
    Serial.println("Playback finished");
    delay(1000);
  }
}
