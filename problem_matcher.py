import json
import string
from collections import defaultdict

def determine_problems(monitor_output):
    transcript = monitor_output["transcript"]
    for character in string.punctuation:
        if character == "'":
            continue
        transcript = transcript.replace(character, ' ')
    transcript_words = transcript.split()

    symptom_database = json.load(open("problem_database/symptom_database.json"))
    symptom_words_list = set()
    for symptom in symptom_database:
        for word in symptom.split():
            symptom_words_list.add(word)

    filtered_transcript_words = []
    for word in transcript_words:
        if word in symptom_words_list:
            filtered_transcript_words.append(word)

    word_pairs = []
    for i in range(0, len(filtered_transcript_words) - 1):
        word_pairs.append(filtered_transcript_words[i] + " " + filtered_transcript_words[i + 1])
        word_pairs.append(filtered_transcript_words[i + 1] + " " + filtered_transcript_words[i])
    transcript_key_phrases = filtered_transcript_words + word_pairs

    problem_frequencies = defaultdict(lambda: 0)
    for phrase in transcript_key_phrases:
        if phrase in symptom_database:
            for problem in symptom_database[phrase]:
                problem_frequencies[problem] += 1
    problem_frequencies = sorted([(problem, problem_frequencies[problem]) for problem in problem_frequencies],
                               key=lambda x: x[1], reverse=True)

    if problem_frequencies:
        problem_severities = json.load(open("problem_database/problem_severities.json"))
        severity = problem_severities[problem_frequencies[0][0]]
        return {"patient_number":monitor_output["patient_number"],
                "timestamp":monitor_output["timestamp"],
                "severity": severity,
                "most_likely_problems":problem_frequencies,
                "transcript": monitor_output["transcript"]}
    else:
        return None


# monitor_output = {'patient_number': 1, 'transcript': 'quick.', 'total_confidence': 0.97021484, 'word_confidences': [0.97021484], 'timestamp': '2022-01-22T17:02:04.958Z'}
# print(determine_problems(monitor_output))
# print(determine_problems({'patient_number': 2, 'transcript':"Help! I fell down the stairs and I am bleeding a lot! Can one of you help me, please? I can't get up.", 'timestamp': '2021-11-23T12:42:54.924Z'}))
# monitor_output = {'patient_number': '1', 'transcript': "help. I fallen over and I can't get up I'm bleeding. One of you come see me, I'm on the floor in the wall by the bed. I don't know what's going on. Help my leg hurts deals if you put in there or just keep talking. Laura ips it did do the Swift brown fox, brown dog", 'total_confidence': 0.8959961, 'word_confidences': [0.9746094, 0.68847656, 0.87597656, 0.97021484, 0.9453125, 0.8959961, 0.95654297, 0.93066406, 0.8989258, 0.77001953, 0.984375, 0.9760742, 0.94677734, 0.9941406, 0.921875, 0.98291016, 0.9892578, 0.8901367, 0.9794922, 0.97998047, 0.99072266, 0.92041016, 0.9433594, 0.30029297, 0.88623047, 0.9868164, 0.90283203, 0.9501953, 0.9746094, 0.9902344, 0.9121094, 0.99121094, 0.9667969, 0.42822266, 0.9428711, 0.96972656, 0.83447266, 0.5395508, 0.6894531, 0.5761719, 0.8798828, 0.75878906, 0.8041992, 0.91064453, 0.98339844, 0.9946289, 0.9946289, 0.33007812, 0.89160156, 0.421875, 0.6899414, 0.67333984, 0.93115234, 0.9682617, 0.97265625, 0.78466797, 0.5361328, 0.52734375], 'timestamp': '2022-01-22T18:35:26.654Z', 'language': 'en-GB'}
# print(determine_problems(monitor_output))

