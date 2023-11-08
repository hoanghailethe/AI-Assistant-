import speech_recognition as sr
# from openai_whisper import Whisper
import openai
# import simpleaudio as sa
# from pydub import AudioSegment
import whisper
import os 
from dotenv import load_dotenv

# record
import pyaudio
import wave

# Set up the OpenAI and Whisper API keys
# Load the API key from an environment variable for security
load_dotenv()  # This loads the environment variables from the .env file
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")
openai.api_key = api_key

def listen_for_wake_word():
    # Initialize the recognizer and microphone
    print('listening')
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            audio = recognizer.listen(source)
            # Use pocketsphinx to detect the wake word
            if recognizer.recognize_sphinx(audio) == 'Wake':
                print('Wake')
                return True
            elif recognizer.recognize_sphinx(audio) == 'Sleep':
                print('Sleep')
                exit()

def record_voice_audio() : 
    print('REcording audioi...')
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "audio.mp3"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_speech_to_text():
    # Use Whisper to transcribe speech
    # You would need to implement the Whisper API call here
    try :
        model = whisper.load_model("base")
        result = model.transcribe("audio.mp3")
        print(result["text"])
        return result["text"]
    except sr.UnknownValueError:
        print("Unknown err")
    except sr.RequestError as e:
        print(f"Could not request results from openAI Speech Recognition service; {e}")
    return "Sorry error happen!!"
        

def send_text_to_chat_gpt(text):
    # Send the transcribed text to OpenAI's ChatGPT and get a response
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                  {"role": "user", "content": text}]
    )
    print(response)
    return response.choices[0].message['content']

def convert_text_to_speech(text):
    # Convert the ChatGPT response to audio using OpenAI's text-to-speech model
    # You would need to implement the OpenAI text-to-speech API call here
    print('convert_text_to_speech ... ')
    

# def play_audio(audio):
#     # Play the audio response
#     sound = AudioSegment.from_file(audio)
#     playback = sa.play_buffer(sound.raw_data, num_channels=1, bytes_per_sample=sound.sample_width, sample_rate=sound.frame_rate)
#     playback.wait_done()

# while True:
    # if listen_for_wake_word():
    #     record_voice_audio()
    #     spoken_text = transcribe_speech_to_text()
    #     chat_response = send_text_to_chat_gpt(spoken_text)
    #     audio_response = convert_text_to_speech(chat_response)
        # play_audio(audio_response)

# pip install -U openai-whisper

record_voice_audio()