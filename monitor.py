# -*- coding: utf-8 -*
# Dependencies
import sys
import os
import sounddevice as sd
import asyncio
import json
import requests
from scipy.io.wavfile import write
from deepgram import Deepgram

#REMEMBER TO ACTIVATE THE RIGHT ENVIROMENT!


if len(sys.argv) == 4:
    print("4 args")
    _, PATIENT_NUMBER, RECORD_TIME_SECONDS, LANGUAGE = sys.argv
elif len(sys.argv) == 3:
    print("3 args")
    _, PATIENT_NUMBER, RECORD_TIME_SECONDS = sys.argv
    print("Language not specified, defaulting to English")
    LANGUAGE = "english"
elif len(sys.argv) == 2:
    print("1 args")
    _, PATIENT_NUMBER = sys.argv
    print("Message length not specified, defaulting to 30 seconds")
    RECORD_TIME_SECONDS = 30
    print("Language not specified, defaulting to English")
    LANGUAGE = "english"
else:
    raise Exception("Please supply a patient number, message time and language")

RECORD_TIME_SECONDS = int(RECORD_TIME_SECONDS)

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


def map_string_to_code(lang_str):
    lower = lang_str.lower()
    out = "en-GB"
    if lower in ["english", "eng", "gb", "british", "uk"]:
        out = "en-GB"
    elif lower in ["french", "fr", "france"]:
        out = "fr"
    elif lower in ["german", "de", "germany"]:
        out = "de"
    elif lower in ["spanish", "spain", "es"]:
        out = "es"
    return out


def record_audio():
    print("Beginning recording...")
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

def reduce_transcript_dict(transcript_dict, lang_code="en-GB"):
    timestamp = transcript_dict["metadata"]["created"]
    data = transcript_dict["results"]["channels"][0]["alternatives"][0]
    transcript = data["transcript"]
    total_confidence = data["confidence"]
    word_dicts = []
    for w_dict in data["words"]:
        word_dicts.append(w_dict)
    out_dict = {"message" : {"patient_number": PATIENT_NUMBER, "transcript": transcript, "total_confidence": total_confidence, 
                "word_confidences": word_dicts, "timestamp": timestamp, "language": lang_code}}
    return out_dict


def send_data(transcribe_dict):
    print("Sending data to Cloud")
    # use JSON kwarg to take dict and send as JSON stream in requests - works for GCP
    status_code = 0
    while status_code != 200:
        print("Server busy, retrying")
        r = requests.post(URL, json=transcribe_dict)
        status_code =int(r.status_code)
    print("Data returned:")
    print(r.text)


async def transcript(): #from DG docs
    recording_successful = -1
    while recording_successful != 0: #loop until we get an audio file
        recording_successful = record_audio()
    print("Recording finished!")

    lang_code = map_string_to_code(LANGUAGE)
    dg_client = Deepgram(API_KEY)
    with open("output.wav", 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = await dg_client.transcription.prerecorded(source, {'punctuate': True, 'language': lang_code,})
        reduced_dict = reduce_transcript_dict(response, lang_code)
        print(reduced_dict["message"]["transcript"])
        send_data(reduced_dict)

asyncio.run(transcript())
