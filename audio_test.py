import RPi.GPIO as GPIO
import pyaudio
import numpy as np

# 設定 GPIO 
BUZZER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 設定 PyAudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

try:
    while True:
        # 讀取音訊數據
        data = stream.read(CHUNK, exception_on_overflow=False)
        
        audio_data = np.frombuffer(data, dtype=np.int16)
        # 計算音量（簡單的振幅檢測）
        volume = np.abs(audio_data).mean()

        # 如果有音量時，啟動LED燈
        if volume > 0:  
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    GPIO.cleanup()
    stream.stop_stream()
    stream.close()
    p.terminate()