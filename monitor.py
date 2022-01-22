# -*- coding: utf-8 -*
# Dependencies
import os
import sounddevice as sd
import asyncio
import json
import requests
from scipy.io.wavfile import write
from deepgram import Deepgram


URL = "https://europe-west2-dementiaassist.cloudfunctions.net/transcription_sentiment"
HOME = os.path.expanduser("~")
DG_API_KEY_PATH = HOME + "/Documents/coding/keys/deepgram.txt"
API_KEY = ""

with open(DG_API_KEY_PATH) as api_file:
    api_list = api_file.read().splitlines() #needed to avoid newlines in api key which cause error

API_KEY = api_list[0]

# Audio params
CHUNK = 1024
CHANNELS = 2
RATE = 44100

RECORD_TIME_SECONDS = 5


def record_audio():
    try:
        myrecording = sd.rec(int(RECORD_TIME_SECONDS * RATE), samplerate=RATE, channels=CHANNELS)
        sd.wait()  # Wait until recording is finished
    except Exception as e:
        print(e)
        return -1

    try:
        write('output.wav', RATE, myrecording)  # Save as WAV file
    except Exception as e:
        print(e)
        return -1
    return 0

def reduce_transcript_dict(transcript_dict):
    data = transcript_dict["results"]["channels"][0]["alternatives"][0]
    transcript = data["transcript"]
    total_confidence = data["confidence"]
    word_confidences = []
    for w_dict in data["words"]:
        word_confidences.append(w_dict["confidence"])
    out_dict = {"transcript": transcript, "total_confidence": total_confidence, 
                "word_confidences": word_confidences}
    return out_dict

def send_data(transcribe_json):
    r = requests.post(URL, data=transcribe_json)

async def transcript(): #from DG docs
    recording_successful = -1
    while recording_successful != 0: #loop until we get an audio file
        recording_successful = record_audio()

    dg_client = Deepgram(API_KEY)
    with open("output.wav", 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = await dg_client.transcription.prerecorded(source, {'punctuate': True})
        reduced_dict = reduce_transcript_dict(response)
        #print(json.dumps(response, indent=4))
        print(reduced_dict)
        send_data(reduced_dict)

asyncio.run(transcript())
