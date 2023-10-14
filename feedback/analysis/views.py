from django.shortcuts import render,HttpResponse
from transformers import pipeline
from moviepy.editor import *
from pydub import AudioSegment
from home.models import Video
import pickle
from google.cloud import speech
from lectures.models import Lectures
import pandas as pd
import plotly.graph_objects as go

# Create your views here.
def home(request):
    filename = 'media/'+str(Video.objects.all()[len(Video.objects.all())-1].video)
    #f = Video.objects.all().reverse()[0].video.open('r')
    audio = VideoFileClip(filename).audio
    audio.write_audiofile('audio/audio.wav')
    audio = AudioSegment.from_wav("audio/audio.wav")
    
    #utterances = calculate_utterances(audio)
    #print(utterances)
    
    file = open('utterances.pkl', 'rb')
    utterances = pickle.load(file)
    file.close()
    
    utterances = clean_utterances(utterances)
    utterances, questions = questions_metric(utterances)
    engage = engagement_score(utterances)
    context = {'questions':questions,'engagement_score':engage,'tone_modulation':0.5,'graph':visualize1(pd.DataFrame(utterances))}
    return render(request,'analysis/home.html',context)

def calculate_utterances(audio):
    utterances = []
    i = 0
    t = 60000*0.5

    pipe_emotion = pipeline("audio-classification", model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")
    #pipe_asr = pipeline("automatic-speech-recognition", model="microsoft/speecht5_asr")

    while (i<len(audio)-t):
        utt_dict = {}
        utt_dict['start_time'] = i
        utt_dict['end_time'] = i+t
        audio[i:i+t].export('audio/temp.wav', format="wav")
        utt_dict['emotion'] = pipe_emotion('audio/temp.wav')
        response = speech_to_text('audio/temp.wav')
        text = ''
        for j, result in enumerate(response.results):
            alternative = result.alternatives[0]
            text+=alternative.transcript
        utt_dict['transcript'] = text
        i+=t
        print(utt_dict)
        utterances.append(utt_dict)        
    return utterances

def clean_utterances(utterances):
    for utterance in utterances:
        max_score = 0
        key_max = ''
        for emotion in utterance['emotion']:
            if (emotion['score']>max_score):
                key_max = emotion['label']
        if (key_max=='fearful' or key_max=='disgust' or key_max=='neutral'):
            key_max = 'non-engaging'
        else:
            key_max='engaging'
        del utterance['emotion']
        utterance['emotion'] = key_max
    return utterances

def questions_metric(utterances):
    pipe = pipeline("text-classification", model="mrsinghania/asr-question-detection")

    questions = 0
    for utterance in utterances:
        utterance['question'] = int(pipe('lol')[0]['label'][-1])
        if utterance['question'] == 1:
            questions+=1

    return utterances, questions
    
def engagement_score(utterances):
    engage_times = 0
    for utterance in utterances:
        if (utterance['emotion']=='engaging'):
            engage_times+=1
    return engage_times/len(utterances)

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

def visualize1(df):
    for count, i in enumerate(df['emotion']):
        if i == 'non-engaging':
            i = 0
        else:
            i = 1
        df.loc[count, 'emotion'] = i

    time_points = {'0': [], '1': []}
    for i, time in enumerate(df['start_time']):
        end_time = df.loc[i, 'end_time']
        gap = end_time - time
        time_points[str(df.loc[i, 'emotion'])].append((time/1000, gap/1000))

    # Calculate the overall time range
    min_time = min(time_points['0'][0][0], time_points['1'][0][0])
    max_time = max(time_points['0'][-1][0], time_points['1'][-1][1])

    # Convert the time range to minutes
    min_time = min_time / 60
    max_time = max_time / 60

    # Create figure
    fig = go.Figure()

    # Add non-engaging bars
    for time_point in time_points['0']:
        x_center = (time_point[0] + time_point[1]) / (2 * 60)  # Center of the interval in minutes
        fig.add_shape(
            type="rect",
            x0=time_point[0] / 60,
            x1=time_point[1] / 60,
            y0=4,
            y1=16,
            line=dict(color="red"),
            fillcolor="red",
            name="Negative",
        )

    # Add engaging bars
    for time_point in time_points['1']:
        x_center = (time_point[0] + time_point[1]) / (2 * 60)  # Center of the interval in minutes
        fig.add_shape(
            type="rect",
            x0=time_point[0] / 60,
            x1=time_point[1] / 60,
            y0=4,
            y1=16,
            line=dict(color="green"),
            fillcolor="green",
            name="Positive",
        )

    fig.update_layout(
        xaxis=dict(
            title='Time (minutes)',
            range=[min_time, max_time],  # Set the initial range to show the full time duration
            tickmode="auto",
            nticks=10,
            tickformat="%H:%M:%S",
        ),
        yaxis=dict(tickvals=[10], ticktext=['Emotion'], range=[0,25]),
        showlegend=True,
        height=300,
        width=800,
    )

    #fig.show()

    return fig.to_html()