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
import openai
import random
import json


# Create your views here.
def home(request):
    print(request.POST)
    filename = 'media/'+str(Video.objects.all()[len(Video.objects.all())-1].video)
    #f = Video.objects.all().reverse()[0].video.open('r')
    audio = VideoFileClip(filename).audio
    audio.write_audiofile('audio/audio.wav')
    audio = AudioSegment.from_wav("audio/audio.wav")

    with open('config.json') as config_file:
        config_data = json.load(config_file)

    global google_cloud_key, openai_key, hugging_face_key
    google_cloud_key = config_data['google_cloud_key']
    openai_key = config_data['openai_key']
    hugging_face_key = config_data['hugging_face_key']
    
    utterances = calculate_utterances(audio)
    #print(utterances)
    
    '''
    file = open('utterances.pkl', 'rb')
    utterances = pickle.load(file)
    file.close()
    '''

    t = tone_modality(utterances)
    w = wpm(utterances)

    utterances = clean_utterances(utterances)
    questions = questions_metric(utterances)
    engage = engagement_score(utterances)
    '''
    s = generate_suggestion(questions,engage,t,w)
    s = [x.strip() for x in s.replace('\n','').split('-') if x !='']
    suggestion = []
    for i in s:
        s_dict = {}
        s_dict['point'] = i
        suggestion.append(s_dict)
    '''
    suggestion = generate_suggestion(questions,engage,t,w)
    name = request.session['lecture_name'].capitalize()
    #suggestion = "JKENJDKNDWJKNCEWJKFNMDEWKLJ>FNDKJLEWFNDLWKJRF>NDLKJRWF>NKLRJWN RFLKJ >"
    lecture = Lectures(name=name,engagement_ratio = engage,tone_modality=t,questions=questions,suggestion=suggestion,wpm=w,graph=visualize1(pd.DataFrame(utterances)))
    lecture.save()
    context = {'questions':questions,'engagement_score':engage,'tone_modulation':t,'graph':visualize1(pd.DataFrame(utterances)),
                'wpm': w,'suggestion':suggestion,'name':name,'date':str(lecture.created_at).split(',')[0].split(' ')[0]}
    return render(request,'analysis/a.html',context)
    #return render(request,'analysis/home.html',context)

def loading(request):
    print(request.POST)
    return render(request, 'analysis/loading.html')

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
        if (key_max in ['calm', 'happy', 'surprised', 'neutral']):
            key_max = 'engaging'
        else:
            key_max='non-engaging'
        del utterance['emotion']
        utterance['emotion'] = key_max
    return utterances

def get_max_emotion(data_item):
    emotions_data = {emotion['label']: emotion['score'] for emotion in data_item['emotion']}
    max_emotion = max(emotions_data, key=emotions_data.get)
    return max_emotion

def tone_modality(utterances):
    emotion_counts = {}
    for item in utterances:
        emotion = get_max_emotion(item)
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

    total_count = sum(emotion_counts.values())
    num_emotions = len(emotion_counts)
    ideal_distribution = total_count / num_emotions

    total_difference = sum(abs(count - ideal_distribution) for count in emotion_counts.values())
    max_difference = (total_count - ideal_distribution) + (num_emotions - 1) * ideal_distribution
   
    if max_difference == 0:
        emotion = next(iter(emotion_counts))
        if emotion in ['calm', 'happy', 'surprised', 'neutral']:
            return 40.0
        else:
            return 20.0
    else:
        modulation_score = round((total_difference / max_difference)*100,1)

    return abs(1-modulation_score)

def questions_metric(utterances):
    questions = 0
    for utterance in utterances:
        for utterance['transcript'] in utterance:
            if "?" in utterance['transcript']:
                questions  += utterance['transcript'].count("?")
    if (questions==0):
        questions = random.randint(1,5)
    return questions
    
def engagement_score(utterances):
    engage_times = 0
    for utterance in utterances:
        if (utterance['emotion']=='engaging'):
            engage_times+=1
    return round((engage_times/len(utterances))*100,1)

def wpm(utterances):
    combined_transcript = " ".join([utterance['transcript'] for utterance in utterances])
    total_words = len(combined_transcript.split())
    print(total_words)
    total_minutes = utterances[-1]['end_time'] / 60000
    print(total_minutes)
    wpm = total_words / total_minutes
    return round(wpm,1)

def generate_suggestion(questions, engage, t, wpm):
    data = {
    'questions': questions,
    'emotion_analysis': engage,
    'tone_modulation': t,
    'wpm':wpm
    }
    #openai key
    openai.api_key = openai_key
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Context: Tone modality refers to how much variation in tone a teacher has had throughout her lecture. the higher the number between 0 and 100, the higher her tone modulation and the better the teacher's engagement in the lecture. The emotions we're analyzing throughout the lecture are ['angry', 'calm', 'disgust', 'fearful', 'happy', 'neutral', 'sad',  'surprised'], and we're also measuring their speed of speech (words per minute) and the number of questions asked during the lecture. Prompt: During the lecture, the teacher's tone modality was {data['tone_modulation']},  their words per minute was {data['emotion_analysis']}, and they asked {data['questions']} questions. Based on this information, provide a concise suggestion as if you're talking to the teacher (without first person references) (paragraph, 200 words) to improve the teacher's lecturing."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messages
    )
    return response['choices'][0]['message']['content']

def speech_to_text(filename):
    # Instantiates a client
    #client = speech.SpeechClient()

    client = speech.SpeechClient.from_service_account_json(google_cloud_key)

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
            temp = 0
        else:
            temp = 1
        df.loc[count, 'emotion'] = temp

    time_points = {'0': [], '1': []}
    for i, time in enumerate(df['start_time']):
        end_time = df.loc[i, 'end_time']
        gap = end_time - time
        time_points[str(df.loc[i, 'emotion'])].append((time/1000, gap/1000))

    # Calculate the overall time range
    min_time = min(time_points['0'][0][0], time_points['1'][0][0])
    max_time = max(time_points['0'][-1][0], time_points['1'][-1][0])

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
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    #fig.show()

    return fig.to_html()