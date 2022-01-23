import problem_matcher as matcher
import json
from google.cloud import translate


patient_data = {}


def respond_to_request(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept',
                'Access-Control-Max-Age': '3600',
            }

    global patient_data

    request_json = request.get_json()

    if request_json and 'message' in request_json:
        print("using JSON") #JSON is always used so put function after here
        patient_message = transcript_to_message(request_json['message'])
        dump_user_data(patient_message)
        return (patient_message, 200, headers)
    elif request_json and 'request' in request_json:
        print(request)
        print("TYPE:", type(request))
        print(request_json)
        print(patient_data)
        if len(patient_data.keys()) > 0:
            return_data = patient_data
            patient_data = {}
            return (json.dumps(return_data), 201, headers)
            #return (return_data, 201, headers)
        else:
            
            return ("No new patient data!", 202, headers)
    else:
        print(request)
        print("TYPE:", type(request))
        print(request_json)
        print(patient_data)
        return ('Error parsing the JSON request', 203, headers)


def transcript_to_message(transcript_dict):
    num = transcript_dict["patient_number"]
    transcript = transcript_dict["transcript"]

    lang = transcript_dict['language']
    if lang != "en-GB": #modify non-english word confidences as they're what's used by the matcher
        transcript_dict["translated"] = translate_text(text=transcript, source_lang_code=lang) #keep this as its useful later
        langauge_setting = "different"
    else:
        transcript_dict["translated"] = ""
        langauge_setting = "same"

    sentiment_parsed = matcher.determine_problems(transcript_dict, lang=langauge_setting)

    problem_list = sentiment_parsed["most_likely_problems"]
    action = sentiment_parsed["action"]
    severity = sentiment_parsed["severity"]
    
    time = transcript_dict["timestamp"]

    message_out = {"patient_number":num, "problem":problem_list, "suggested_action":action, 
                   "severity":severity, "full_text":transcript, "time": time, "translated":transcript_dict["translated"]}
    return message_out

def dump_user_data(message):
    global patient_data
    patient = "patient" + message["patient_number"]
    if patient not in patient_data.keys():
        patient_data[patient] = [message]
    else:
        patient_data[patient].append(message)

def translate_text(text="Hello, world!", project_id="dementiaassist", source_lang_code="fr"):
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_lang_code,
            "target_language_code": "en-GB",
        }
    )
    translated_text = ""
    for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text))
        translated_text += translation.translated_text
    return translated_text