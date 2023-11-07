import os
import time
import pyaudio
import speech_recognition as sr
import playsound 
from gtts import gTTS
import openai


lang ='vi'

openai.api_key = api_key


guy = ""

while True:
    def get_adio():
        print('Start running')
        r = sr.Recognizer()
        with sr.Microphone( device_index= 1 )  as source:
            print('Start LISTENING')
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
                global guy 
                guy = said
                

                if "Friday" in said:
                    words = said.split()
                    new_string = ' '.join(words[1:])
                    print(new_string) 
                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content":said}])
                    text = completion.choices[0].message.content
                    speech = gTTS(text = text, lang=lang, slow=False, tld="com.au")
                    speech.save("welcome1.mp3")
                    playsound.playsound("welcome1.mp3")

            except Exception:
                print("Exception")


        return said

    if "stop" in guy:
        break


    get_adio()
    
    
# def record_audio() :
#     #load all audio input devices 
#     for index, device in enumerate(PvRecorder.get_audio_devices()):
#         print(f"[{index}] {device}")
        
#     recorder = PvRecorder(device_index=2, frame_length=512) #(32 milliseconds of 16 kHz audio)
#     audio = []
#     path = 'audio_recording.wav'

#     try:
#         recorder.start()


#         while True:
#             frame = recorder.read()
#             audio.extend(frame)
#     except KeyboardInterrupt:
#         recorder.stop()
#         with wave.open(path, 'w') as f:
#             f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
#             f.writeframes(struct.pack("h" * len(audio), *audio))
#     finally:
#         recorder.delete()

# !pip install --upgrade pip
# !pip install openai
# pip install --upgrade openai

# pip install pipwin
# pipwin install pyaudio

# pip uninstall --pre openai  
# C:\Users\lethe\AppData\Local\Programs\Python\Python311\