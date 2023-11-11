import os
import wave
import speech_recognition as sr
import playsound
from gtts import gTTS
import openai
import uuid
import pyaudio
from pydub import AudioSegment

from dotenv import load_dotenv

import mutagen 
from mutagen.wave import WAVE 

import ffmpeg  
import shutil

load_dotenv()  # This loads the environment variables from the .env file

# Load the API key from an environment variable for security
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key

# Language settings
lang = 'vi'  # Vietnamese

def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()
    # List all microphones
    print("Available microphones:")
    for index, name in enumerate(mic_list): 
        print(f"{index}: {name}")
    mic_index = int(input("Select the microphone index: "))
    return mic_index

def get_audio(mic_index):
    print('Listening...')
    r = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=mic_index) as source:
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = r.listen(source, phrase_time_limit=10)

            text = ""
            # Recognize speech using Google Speech Recognition
            text = r.recognize_google(audio, language=lang)
            print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return text

def respond_to_audio(text):
    if "Friday" in text:
        words = text.split()
        new_string = ' '.join(words[1:])
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_string}])
        response_text = completion.choices[0].message.content
        speech = gTTS(text=response_text, lang=lang, slow=False)
        file_name = f"response_{uuid.uuid4().hex}.mp3"
        speech.save(file_name)
        playsound.playsound(file_name)
        os.remove(file_name)  # Clean up the file after playing

def run () :
    while True:
        # Main code
        mic_index = list_microphones()  # Get the list of microphones and ask the user to choose one
        spoken_text= get_audio(mic_index)  # Pass the selected microphone index to get_aud
        if "stop" in spoken_text.lower():
            print("Stopping the voice assistant.")
            break
        if spoken_text:
            respond_to_audio(spoken_text)
        
        
# pip install -r requirements.txt

def run_test_module() : 
    # Convert m4a to wav
    # audio = AudioSegment.from_file("test.m4a", format="m4a")
    # audio.export("test.wav", format="wav")
    
    file_test = "phamNhanTuTien.mp3"
    spoken_text= test_solo_audio(file_test)  # Pass the selected microphone index to get_aud
    
    if "stop" in spoken_text.lower():
        print("Stopping the voice assistant.")
        
    if spoken_text:
        respond_to_audio(spoken_text)

def test_solo_audio(audio_file_path):
    # Initialize the recognizer
    r = sr.Recognizer()

    # check duratrion > 10 -> trim only 10 seconds
    # audio_output = trim_audio_first_30sec(audio_file_path)
    
    # Set the maximum duration for recognition (in seconds)
    max_duration = 20
    
    # Use the audio file as the audio source
    with sr.AudioFile(audio_file_path) as source:
        # Listen for the data (load audio to memory)
        audio_data = r.record(source, duration=max_duration)
        # Recognize (convert from speech to text)
        try:
            # Specify the language
            text = r.recognize_google(audio_data, language="vi-VN")
            print(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        
def trim_audio_first_30sec(audio_file_path):
    voice = WAVE(audio_file_path)
    voice_info = voice.info
    voice_length = voice_info.length
    audio_output = None
    if voice_length > 10 :
        audio_input = ffmpeg.input('input.mp3')
        audio_cut = audio_input.audio.filter('atrim', duration=10)
        audio_output = ffmpeg.output(audio_cut, 'input_audio.mp3')
        ffmpeg.run(audio_output)
    else :
        audio_output = shutil.copy2(audio_file_path, 'input_audio.mp3')
    return audio_output
        
# run test once
run_test_module()