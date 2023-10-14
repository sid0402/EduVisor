from moviepy.editor import *
from pydub import AudioSegment
from speechbrain.pretrained.interfaces import foreign_class
import requests
from transformers import pipeline
import os
from google.cloud import speech
import pickle

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "hackgt-audio-9ba4eb05b9b2.json"
client = speech.SpeechClient.from_service_account_json('hackgt-audio-9ba4eb05b9b2.json')

#extracting audio from video 
#exports to mp3

video = VideoFileClip('media/5-_Minute_Lecture__Professor_Irwin_Goldman.mp4')
audio = video.audio
audio.write_audiofile('audio/test.wav')

TOKENIZERS_PARALLELISM=False

audio = AudioSegment.from_wav("audio/audio.wav")
#seg = audio[0:30000]
#seg.export('audio/test_seg.wav', format="wav")

'''
auth_token = "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"
classifier = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP", pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")
'''


def speech_to_text(filename):
    # Instantiates a client
    #client = speech.SpeechClient()

    client = speech.SpeechClient.from_service_account_json('hackgt-audio-9ba4eb05b9b2.json')

    with open(filename,'rb') as f:
        audio_data = f.read()

    # The name of the audio file to transcribe
    #gcs_uri = filename

    audio = speech.RecognitionAudio(content=audio_data)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        sample_rate_hertz = 44100,
        audio_channel_count = 2,
        enable_automatic_punctuation=True
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    
    return response

#print(speech_to_text('audio/test_seg.wav').alternatives[0].transcript)
'''
response = speech_to_text('audio/test_seg.wav')
text = ''
for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    text+=alternative.transcript
    print("-" * 20)
    print(f"First alternative of result {i}")
    print(f"Transcript: {alternative.transcript}")
#print(response.results.alternatives[0].transcript)

print(text)
'''

segments = []
emotions = []

utterances = []

i = 0
t = 60000*0.5
print(len(audio))

pipe = pipeline("audio-classification", model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")
#pipe2 = pipeline("automatic-speech-recognition", model="microsoft/speecht5_asr")

while (i<len(audio)-t):
    utt_dict = {}
    utt_dict['start_time'] = i
    utt_dict['end_time'] = i+t
    #segments.append(audio[i:i+t])
    audio[i:i+t].export('audio/temp.wav', format="wav")
    utt_dict['emotion'] = pipe('audio/temp.wav')
    #emotions.append(pipe('audio/temp.wav'))
    response = speech_to_text('audio/temp.wav')
    text = ''
    for j, result in enumerate(response.results):
        alternative = result.alternatives[0]
        text+=alternative.transcript
    utt_dict['transcript'] = text
    #utt_dict['transcript']=pipe2('audio/temp.wav')
    #utt_dict['transcript'] = speech_to_text('audio/temp.wav')
    i+=t
    print(utt_dict)
    utterances.append(utt_dict)
    print(i)

# For loading
file = open('utterances.pkl','wb')
pickle.dump(utterances,file)
file.close()

print(utterances)