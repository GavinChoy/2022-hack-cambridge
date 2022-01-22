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


monitor_output = {'patient_number': 1, 'transcript': 'quick.', 'total_confidence': 0.97021484, 'word_confidences': [0.97021484], 'timestamp': '2022-01-22T17:02:04.958Z'}
print(determine_problems(monitor_output))
print(determine_problems({'patient_number': 2, 'transcript':"Help! I fell down the stairs and I am bleeding a lot! Can one of you help me, please? I can't get up.", 'timestamp': '2021-11-23T12:42:54.924Z'}))

