import json
from collections import defaultdict


original_database_file = open("problem_database.json")

symptoms_for_each_problem = json.load(original_database_file)["problems"]

problems_for_each_symptom = defaultdict(lambda: set())
severity_for_each_problem = {}
action_for_each_problem= {}

for problem in symptoms_for_each_problem:
    severity_for_each_problem[problem["problem"]] = problem["severity"]
    action_for_each_problem[problem["problem"]] = problem["action"]
    for symptom in problem["symptoms"]:
        problems_for_each_symptom[symptom].add(problem["problem"])


for symptom in problems_for_each_symptom:
    problems_for_each_symptom[symptom] = list(problems_for_each_symptom[symptom])

def determine_problems(monitor_output):
    words_and_confidences = []
    for word_confidence in monitor_output["word_confidences"]:
        words_and_confidences.append((word_confidence["word"], word_confidence["confidence"]))

    symptom_database = problems_for_each_symptom #json.load(open("problem_database/symptom_database.json"))
    symptom_words_list = set()
    for symptom in symptom_database:
        for word in symptom.split():
            symptom_words_list.add(word)

    filtered_words_confidences = []
    for word_and_confidence in words_and_confidences:
        if word_and_confidence[0] in symptom_words_list:
            filtered_words_confidences.append(word_and_confidence)

    word_and_confidence_pairs = []
    for i in range(0, len(filtered_words_confidences) - 1):
        mean_confidence = 0.5 * (filtered_words_confidences[i][1] + filtered_words_confidences[i + 1][1])
        word_and_confidence_pairs.append((filtered_words_confidences[i][0] + " " + filtered_words_confidences[i + 1][0], mean_confidence))
        word_and_confidence_pairs.append((filtered_words_confidences[i + 1][0] + " " + filtered_words_confidences[i][0], mean_confidence))
    transcript_key_phrases = filtered_words_confidences + word_and_confidence_pairs

    problem_frequencies = defaultdict(lambda: 0)
    problem_severity_weights = defaultdict(lambda: 0.0)
    for phrase in transcript_key_phrases:
        if phrase[0] in symptom_database:
            for problem in symptom_database[phrase[0]]:
                problem_frequencies[problem] += 1
                problem_severity_weights[problem] += phrase[1]
    problem_frequencies = sorted([(problem, problem_frequencies[problem]) for problem in problem_frequencies],
                               key=lambda x: x[1], reverse=True)

    if problem_frequencies:
        problem_severities = severity_for_each_problem #json.load(open("problem_database/problem_severities.json"))
        severity = 0
        total_severity_weight = 0
        for problem in problem_severity_weights:
            total_severity_weight += problem_severity_weights[problem]
            severity += problem_severities[problem] * problem_severity_weights[problem]
        severity = severity / total_severity_weight
        actions=[]
        for (problem, freq) in problem_frequencies:
            action=action_for_each_problem[problem]
            actions.append((problem, action))



        return {"patient_number":monitor_output["patient_number"],
                "timestamp":monitor_output["timestamp"],
                "severity": severity,
                "most_likely_problems":problem_frequencies,
                "transcript": monitor_output["transcript"],
                "action":actions}
    else:
        return None


#monitor_output = {'patient_number': 1, 'transcript': 'quick.', 'total_confidence': 0.97021484, 'word_confidences': [0.97021484], 'timestamp': '2022-01-22T17:02:04.958Z'}
#print(determine_problems(monitor_output))
# print(determine_problems({'patient_number': 2, 'transcript':"Help! I fell down the stairs and I am bleeding a lot! Can one of you help me, please? I can't get up.", 'timestamp': '2021-11-23T12:42:54.924Z'}))
# monitor_output = {'patient_number': '1', 'transcript': "Help I fall nova I can't get up. And one of you please come help me. I'm by the wall on the floor in the room. I'm on ward three and the Snow fox forwards. My leg", 'total_confidence': 0.90722656, 'word_confidences': [{'word': 'help', 'start': 1.3351449, 'end': 1.6938405, 'confidence': 0.9863281, 'punctuated_word': 'Help'}, {'word': 'i', 'start': 1.7735506, 'end': 2.052536, 'confidence': 0.7841797, 'punctuated_word': 'I'}, {'word': 'fall', 'start': 2.052536, 'end': 2.2916665, 'confidence': 0.50439453, 'punctuated_word': 'fall'}, {'word': 'nova', 'start': 2.2916665, 'end': 2.7300723, 'confidence': 0.5073242, 'punctuated_word': 'nova'}, {'word': 'i', 'start': 2.7699275, 'end': 3.048913, 'confidence': 0.9453125, 'punctuated_word': 'I'}, {'word': "can't", 'start': 3.048913, 'end': 3.3278983, 'confidence': 0.98095703, 'punctuated_word': "can't"}, {'word': 'get', 'start': 3.3278983, 'end': 3.4873188, 'confidence': 0.9785156, 'punctuated_word': 'get'}, {'word': 'up', 'start': 3.4873188, 'end': 3.9655795, 'confidence': 0.9580078, 'punctuated_word': 'up.'}, {'word': 'and', 'start': 4.125, 'end': 4.28442, 'confidence': 0.46606445, 'punctuated_word': 'And'}, {'word': 'one', 'start': 4.28442, 'end': 4.4039855, 'confidence': 0.94628906, 'punctuated_word': 'one'}, {'word': 'of', 'start': 4.4039855, 'end': 4.5235505, 'confidence': 0.9042969, 'punctuated_word': 'of'}, {'word': 'you', 'start': 4.5235505, 'end': 4.762681, 'confidence': 0.99121094, 'punctuated_word': 'you'}, {'word': 'please', 'start': 4.762681, 'end': 5.0416665, 'confidence': 0.98828125, 'punctuated_word': 'please'}, {'word': 'come', 'start': 5.0416665, 'end': 5.280797, 'confidence': 0.81103516, 'punctuated_word': 'come'}, {'word': 'help', 'start': 5.280797, 'end': 5.5597825, 'confidence': 0.90722656, 'punctuated_word': 'help'}, {'word': 'me', 'start': 5.5597825, 'end': 5.6793475, 'confidence': 0.9746094, 'punctuated_word': 'me.'}, {'word': "i'm", 'start': 5.878623, 'end': 6.2373185, 'confidence': 0.43823242, 'punctuated_word': "I'm"}, {'word': 'by', 'start': 6.2373185, 'end': 6.396739, 'confidence': 0.7495117, 'punctuated_word': 'by'}, {'word': 'the', 'start': 6.396739, 'end': 6.596014, 'confidence': 0.9584961, 'punctuated_word': 'the'}, {'word': 'wall', 'start': 6.596014, 'end': 6.9148545, 'confidence': 0.9916992, 'punctuated_word': 'wall'}, {'word': 'on', 'start': 6.9148545, 'end': 7.03442, 'confidence': 0.9838867, 'punctuated_word': 'on'}, {'word': 'the', 'start': 7.03442, 'end': 7.3134055, 'confidence': 0.9863281, 'punctuated_word': 'the'}, {'word': 'floor', 'start': 7.3134055, 'end': 7.4329705, 'confidence': 0.9980469, 'punctuated_word': 'floor'}, {'word': 'in', 'start': 7.4329705, 'end': 7.552536, 'confidence': 0.9291992, 'punctuated_word': 'in'}, {'word': 'the', 'start': 7.552536, 'end': 7.8315215, 'confidence': 0.9838867, 'punctuated_word': 'the'}, {'word': 'room', 'start': 7.8315215, 'end': 8.070652, 'confidence': 0.9975586, 'punctuated_word': 'room.'}, {'word': "i'm", 'start': 8.525001, 'end': 8.965, 'confidence': 0.96728516, 'punctuated_word': "I'm"}, {'word': 'on', 'start': 8.965, 'end': 9.245, 'confidence': 0.9165039, 'punctuated_word': 'on'}, {'word': 'ward', 'start': 9.245, 'end': 9.725, 'confidence': 0.9003906, 'punctuated_word': 'ward'}, {'word': 'three', 'start': 9.725, 'end': 10.085, 'confidence': 0.85791016, 'punctuated_word': 'three'}, {'word': 'and', 'start': 10.085, 'end': 10.325001, 'confidence': 0.7426758, 'punctuated_word': 'and'}, {'word': 'the', 'start': 10.325001, 'end': 10.405001, 'confidence': 0.96728516, 'punctuated_word': 'the'}, {'word': 'snow', 'start': 10.565001, 'end': 10.845, 'confidence': 0.9223633, 'punctuated_word': 'Snow'}, {'word': 'fox', 'start': 10.845, 'end': 11.285, 'confidence': 0.7006836, 'punctuated_word': 'fox'}, {'word': 'forwards', 'start': 11.285, 'end': 11.785, 'confidence': 0.5541992, 'punctuated_word': 'forwards.'}, {'word': 'my', 'start': 12.725, 'end': 12.885, 'confidence': 0.98583984, 'punctuated_word': 'My'}, {'word': 'leg', 'start': 12.885, 'end': 13.0, 'confidence': 0.81591797, 'punctuated_word': 'leg'}], 'timestamp': '2022-01-22T18:54:41.491Z', 'language': 'en-GB'}
# print(determine_problems(monitor_output))
#
# print("-------------------------------------------------")
# 
#monitor_output = {'patient_number': '1', 'transcript': "help I fallen over and I've got a headache and I'm vomiting and it's everywhere I in the wall by the corner", 'total_confidence': 0.9658203, 'word_confidences': [{'word': 'help', 'start': 1.06, 'end': 1.5, 'confidence': 0.9584961, 'punctuated_word': 'help'}, {'word': 'i', 'start': 1.54, 'end': 1.8199999, 'confidence': 0.6694336, 'punctuated_word': 'I'}, {'word': 'fallen', 'start': 1.8199999, 'end': 2.1399999, 'confidence': 0.9921875, 'punctuated_word': 'fallen'}, {'word': 'over', 'start': 2.1399999, 'end': 2.6399999, 'confidence': 0.9873047, 'punctuated_word': 'over'}, {'word': 'and', 'start': 2.98, 'end': 3.06, 'confidence': 0.9584961, 'punctuated_word': 'and'}, {'word': "i've", 'start': 3.1, 'end': 3.26, 'confidence': 0.9326172, 'punctuated_word': "I've"}, {'word': 'got', 'start': 3.26, 'end': 3.3799999, 'confidence': 0.9658203, 'punctuated_word': 'got'}, {'word': 'a', 'start': 3.3799999, 'end': 3.5, 'confidence': 0.9707031, 'punctuated_word': 'a'}, {'word': 'headache', 'start': 3.5, 'end': 4.0, 'confidence': 0.9995117, 'punctuated_word': 'headache'}, {'word': 'and', 'start': 4.3399997, 'end': 4.66, 'confidence': 0.95654297, 'punctuated_word': 'and'}, {'word': "i'm", 'start': 4.74, 'end': 5.06, 'confidence': 0.9536133, 'punctuated_word': "I'm"}, {'word': 'vomiting', 'start': 5.06, 'end': 5.56, 'confidence': 0.9975586, 'punctuated_word': 'vomiting'}, {'word': 'and', 'start': 6.1, 'end': 6.22, 'confidence': 0.9511719, 'punctuated_word': 'and'}, {'word': "it's", 'start': 6.22, 'end': 6.72, 'confidence': 0.9067383, 'punctuated_word': "it's"}, {'word': 'everywhere', 'start': 7.18, 'end': 7.68, 'confidence': 0.99365234, 'punctuated_word': 'everywhere'}, {'word': 'i', 'start': 8.0199995, 'end': 8.175, 'confidence': 0.796875, 'punctuated_word': 'I'}, {'word': 'in', 'start': 8.352065, 'end': 8.548804, 'confidence': 0.99365234, 'punctuated_word': 'in'}, {'word': 'the', 'start': 8.548804, 'end': 8.784891, 'confidence': 0.99072266, 'punctuated_word': 'the'}, {'word': 'wall', 'start': 8.784891, 'end': 9.284891, 'confidence': 0.98046875, 'punctuated_word': 'wall'}, {'word': 'by', 'start': 9.296413, 'end': 9.493153, 'confidence': 0.9760742, 'punctuated_word': 'by'}, {'word': 'the', 'start': 9.493153, 'end': 9.729239, 'confidence': 0.99121094, 'punctuated_word': 'the'}, {'word': 'corner', 'start': 9.729239, 'end': 10.0, 'confidence': 0.9941406, 'punctuated_word': 'corner'}], 'timestamp': '2022-01-22T19:21:52.273Z', 'language': 'en-GB'}
#print(determine_problems(monitor_output))
