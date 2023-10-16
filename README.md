# EduVisor

## What it does
EduVisor helps educators have the opportunity to consistently submit their lectures for analysis. Our sophisticated AI-driven evaluation mechanism analyzes both voice & transcript, and offers personalized insights into their teaching methods. By assessing aspects like speech emotions, tone modulation, class engagement, and voice pace, we ensure that teachers can truly resonate with and captivate their students. We also leverage Large Language Models to provide the necessary recommendations to teachers.

## How we built it
The application is built with the Django web framework for the backend and HTML, CSS and JavaScript for the front-end. The lecture videos that were uploaded were split into chunks of 30 seconds using Python's pydub library. These chunks, or utterances, were first fed into the wav2vec speech emotion recognition model through Hugging Face, and then transcribed through Google Cloud Platform's Speech-to-Text model. We performed various operations on these processed utterances to extract our insights. This was finally fed into the GPT-4 API in order to generate recommendations for the educators. The application was connected to the Django ORM, which is Django's built-in database functionality that is operated through MySQL.

## Project Screenshots & Video
<iframe width="560" height="315" src="https://www.youtube.com/embed/acVxFY_FH6o?si=ctbSVkE4rkFkMkaC" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
![Screen Shot 2023-10-15 at 7 44 47 AM](https://github.com/sid0402/EduVisor/assets/36813259/318e7ae1-90cd-44fd-8ad7-15cf0bcaac7d)
![Screen Shot 2023-10-15 at 7 44 25 AM](https://github.com/sid0402/EduVisor/assets/36813259/fc5658e6-f672-4155-b414-94799dd822ee)
