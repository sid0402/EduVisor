import pickle
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
from transformers import pipeline

file = open('utterances.pkl','rb')

utterances = pickle.load(file)
file.close()

#finding main emotion
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

#SENTIMENT ANALYSIS GRAPH
def visualize1(df):
    for count,i in enumerate(df['emotion']):
        if i=='non-engaging':
            i = 0
        else:
            i=1
        df.loc[count,'emotion'] = i
    print(df)

    time_points = {'0':[],'1':[]}
    for i, time in enumerate(df['start_time']):
        end_time = df.loc[i,'end_time']
        gap = end_time-time
        time_points[str(df.loc[i,'emotion'])].append((time,gap))
    print(time_points)
        
    fig, ax = plt.subplots()
    #non-engaging
    ax.broken_barh(time_points['0'], (10, 10), facecolors='tab:red')
    #engaging
    ax.broken_barh(time_points['1'], (10, 10), facecolors='tab:green')
    ax.set_ylim(0, 30)
    ax.set_xlim(0, end_time)
    ax.set_xlabel('Time(s)')
    #ax.set_yticks([2.5,7.5,12.5], labels=['Negative', 'Neutral','Positive'])
    ax.set_yticks([15],labels=['Emotion'])
    #ax.grid(True)
    red_patch = mpatches.Patch(color='red', label='Negative')
    green_patch = mpatches.Patch(color='green', label='Positive')
    plt.legend(handles=[red_patch,green_patch])
    plt.show()

    '''
    fname = fanalysis.split('/')[-1]
    fname = fname.split('.')[0]
    plt.savefig("images/"+str(fname)+'.jpg')
    '''

    return time_points

time_points = visualize1(pd.DataFrame(utterances))

pipe = pipeline("text-classification", model="mrsinghania/asr-question-detection")

questions = 0
for utterance in utterances:
    utterance['question'] = int(pipe('lol')[0]['label'][-1])
    if utterance['question'] == 1:
        questions+=1
        
print(questions)