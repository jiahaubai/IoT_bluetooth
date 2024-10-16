import RPi.GPIO as GPIO
import pyaudio
import numpy as np

# 設定 GPIO 引腳
BUZZER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 設定 PyAudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

# 開啟音訊流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

try:
    while True:
        # 讀取音訊數據
        data = stream.read(CHUNK, exception_on_overflow=False)
        # 將音訊數據轉換為 numpy 陣列
        audio_data = np.frombuffer(data, dtype=np.int16)
        # 計算音量（簡單的振幅檢測）
        volume = np.abs(audio_data).mean()

        # 如果音量超過某個閾值，則啟動蜂鳴器
        if volume > 1000:  # 根據需要調整這個閾值
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    # 清理 GPIO 設置
    GPIO.cleanup()
    # 停止音訊流
    stream.stop_stream()
    stream.close()
    p.terminate()