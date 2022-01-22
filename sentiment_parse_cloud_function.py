import problem_matcher as matcher


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
    request_json = request.get_json()
    print(request)
    print(request_json)
    if request_json and 'message' in request_json:
        print("using JSON") #JSON is always used so put function after here
        #print(request_json['message'])
        patient_message  = transcript_to_message(request_json['message'])
        dump_user_data(patient_message)
        return patient_message
    else:
        return f'Error parsing the JSON request'


def transcript_to_message(transcript_dict):
    num = transcript_dict["patient_number"]
    sentiment_parsed = matcher.determine_problems(transcript_dict)

    problem_list = sentiment_parsed["most_likely_problems"]
    action = []
    severity = sentiment_parsed["severity"]
    text = transcript_dict["transcript"]
    time = transcript_dict["timestamp"]

    message_out = {"patient_number":num, "problem":problem_list, "suggested_action":action, 
                   "severity":severity, "full_text":text, "time": time}
    return message_out

def dump_user_data(message):
    patient = "patient" + message["patient_number"]
    if patient not in patient_data.keys():
        patient_data[patient] = [message]
    else:
        patient[patient].append(message)
