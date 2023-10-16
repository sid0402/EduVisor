# EduVisor

## What it does
EduVisor helps educators have the opportunity to consistently submit their lectures for analysis. Our sophisticated AI-driven evaluation mechanism analyzes both voice & transcript and offers personalized insights into their teaching methods. By assessing aspects like speech emotions, tone modulation, class engagement, and voice pace, we ensure that teachers can truly resonate with and captivate their students. We also leverage Large Language Models to provide the necessary recommendations to teachers.

## How we built it
The application is built with the Django web framework for the backend and HTML, CSS and JavaScript for the front-end. The lecture videos that were uploaded were split into chunks of 30 seconds using Python's pydub library. These chunks, or utterances, were first fed into the wav2vec speech emotion recognition model through Hugging Face, and then transcribed through Google Cloud Platform's Speech-to-Text model. We performed various operations on these processed utterances to extract our insights. This was finally fed into the GPT-3.5-turbo API in order to generate recommendations for the educators. The application was connected to the Django ORM, which is Django's built-in database functionality that is operated through MySQL.

## Project Screenshots & Video
[Watch the video](https://youtu.be/acVxFY_FH6o?si=EZ737nJ70-gSSzw-)
<img width="1512" alt="Screen Shot 2023-10-15 at 11 35 51 PM" src="https://github.com/sid0402/EduVisor/assets/36813259/35fd064a-a74a-4307-ba45-790459bf528d">
![Screen Shot 2023-10-15 at 7 44 47 AM](https://github.com/sid0402/EduVisor/assets/36813259/318e7ae1-90cd-44fd-8ad7-15cf0bcaac7d)
![Screen Shot 2023-10-15 at 7 44 25 AM](https://github.com/sid0402/EduVisor/assets/36813259/fc5658e6-f672-4155-b414-94799dd822ee)

# Installation and Configuration
Create a virtual environment after cloning the repository. Then run the following command, which installs all the python libraries with their specific versions that are used in the project.

```
pip install -r requirements.txt
```

All the applications and code are inside the 'feedback' folder. Navigate to this directory once the virtual environment is created.

## Setting Up API Keys

To use this project, you need to obtain and configure the following API keys:
1. Google Cloud Platform Service Account Key
2. OpenAI API Key
3. Hugging Face API Key

### Configuration

Once you have obtained these API keys, you need to configure them for this project. Add the API keys to the `config.json` file, located in 'feedback', following this format:

```json
{
  "google_cloud_key": "your_google_cloud_key.json",
  "openai_key": "your_openai_key",
  "hugging_face_key": "your_hugging_face_key"
}
```

## Running the application
To run the application on your computer (http://localhost:8000/), run the following code in the feedback directory.
```
python manage.py runserver
```
