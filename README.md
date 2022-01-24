# Doc-com

## 2022-hack-cambridge
Devpost submission for Hack Cambridge Atlas: https://devpost.com/software/efficient-nurses

## Inspiration
Hospitals have had an emergency cord for a while now: pull to be put on hold and eventually talk to a nurse to explain the problem. What if there was an automated solution to this that let patients report their symptoms either on an emergency or check-up basis? This automated solution would then allow nurses to optimize their resources and time dealing with problems in the most efficient way, shortening the time between symptom and solution. This is especially useful due to the shortage of medical professionals as a result of COViD-19 and an ageing population.

## What it does
A Python script (emulating an emergency cord/button or hourly check in) records the patient’s audio and pings the DeepGram API to get a text transcription. This transcription is then sent to a Google Cloud Function for sentiment analysis, which picks out key symptoms from a database, finds associated root causes, severity and solutions. This data is then sent to a live dashboard that nurses can view and make decisions based on real-time patient data.

The system also has the benefit of geo-locating the incidents, which allows for the closest nurses to respond quickly and automatically translating foreign language reports before picking out symptoms, fixing the language barrier communication problem in hospitals.

## How we built it
Python for the ‘Patient Alert’ system: audio recording, DeepGraph SDK and POST requests to our Google Cloud Function.\
Google Cloud function running Python for the text -> symptom sentiment analysis.\
React-JS, CSS, HTML for the front-end scheduling dashboard/monitoring system.

## Challenges we ran into
CORS headers to and from Google Cloud Functions!\
Getting Google Cloud Translate API working in the cloud environment\
Choosing the right Python Audio library (classic pulse-audio problems)

## Accomplishments that we're proud of
Integrating DeepGram (especially the foriegn language transcriptions) into the system in a ‘plug in and play’ way.\
Managing the long cloud deploy times before testing a function.

## What we learned
CORS is hard.\
APIs are good!

## What's next for Doc-com
Making more visualization options for the dashboard\
Allowing nurses and doctors to add their own symptoms, root causes and actions, and share these with others - creating a growing dataset using shared institutional knowledge

## Video demonstrations

English transcription demo:\
[![English transcription demo](https://img.youtube.com/vi/_Z9enlAr-xI/0.jpg)](https://www.youtube.com/watch?v=_Z9enlAr-xI "English transcription demo")

Spanish transcription demo:\
[![English transcription demo](https://img.youtube.com/vi/7h5jPzRJqoQ/0.jpg)](https://www.youtube.com/watch?v=7h5jPzRJqoQ "English transcription demo")