import pickle
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
from transformers import pipeline
import plotly.graph_objects as go

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

#time_points = visualize1(pd.DataFrame(utterances))

#pipe = pipeline("text-classification", model="mrsinghania/asr-question-detection")
'''
questions = 0
for utterance in utterances:
    utterance['question'] = int(pipe('lol')[0]['label'][-1])
    if utterance['question'] == 1:
        questions+=1
        
print(questions)
'''
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

    fig.show()

    fig.write_html("media/plotly_figure.html")

# Example usage:
# Assuming you have a DataFrame df with columns 'start_time', 'end_time', and 'emotion'
# visualize1(df)


# Example usage:
# Assuming you have a DataFrame df with columns 'start_time', 'end_time', and 'emotion'
# visualize1(df)


# Example usage:
# Assuming you have a DataFrame df with columns 'start_time', 'end_time', and 'emotion'
visualize1(pd.DataFrame(utterances))
print(pd.DataFrame(utterances))