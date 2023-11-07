import os
import speech_recognition as sr
import playsound
from gtts import gTTS
import openai
import uuid

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
    with sr.Microphone(device_index=mic_index) as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = r.listen(source)

        text = ""
        try:
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

while True:
    # Main code
    mic_index = list_microphones()  # Get the list of microphones and ask the user to choose one
    spoken_text= get_audio(mic_index)  # Pass the selected microphone index to get_aud
    if "stop" in spoken_text.lower():
        print("Stopping the voice assistant.")
        break
    if spoken_text:
        respond_to_audio(spoken_text)