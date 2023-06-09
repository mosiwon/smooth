# Smart Moolight Speaker

### 스마트 무드등 스피커 (스무스) 는 사용자의 얼굴 표정을 분석하여 해당 감정에 맞는 음악과 LED색상을 자동으로 변경해주는 어플리케이션 입니다.

---
![20230409_153023](https://user-images.githubusercontent.com/61589097/230812177-1df3f1f7-cdd2-4abc-a407-f7cb1571fe81.jpg)
---

- ## 기능

  1. 카메라를 통해 사용자의 얼굴 표정을 실시간으로 인식하여 감정분석

  2. 인식된 감정에 맞는 음악재생

  3. 인식된 감정에 맞는 LED 색상 출력

  4. 현재시각과 감정상태 LCD를 통하여 출력

  5. 사용자 선텍에 따른 음악과 LED 색상 출력

---

- ## 사용 방법

  1. 아두이노 라이브러리 설치 (lib/esp32 파일)

  2. 스마트 무드등 스피커 gui 실행 (smooth.py)

  3. esp 보드 서버에 ip로 연결

  4. 연결과 동시에 카메라를 사용하여 얼굴 인식과 감정 딥러닝 진행

  5. 감정에 따른 음악과 LED 색상 자동 변경

  6. LED 색상과 음악을 사용자가 선택하여 직접 변경

---

- ## 파이썬 라이브러리
  - PyQt6
  - OpenCV
  - Mediapipe
  - HSEmotionRecognizer
  - PyGame
  - Mutagen

---

Link: [https://youtu.be/1LblZCtIPxc](https://youtu.be/1LblZCtIPxc)