import json
import string
from collections import Counter
from collections import defaultdict

transcript = "Help! I fell down the stairs and I am bleeding a lot! Can one of you help me, please? I can't get up."

for character in string.punctuation:
    if character == "'":
        continue
    transcript = transcript.replace(character, ' ')

transcript_words = transcript.split()

print(transcript_words)

symptom_database = json.load(open("problem_database/symptom_database.json"))

symptom_words_list = set()

print(symptom_database)

for symptom in symptom_database:
    for word in symptom.split():
        symptom_words_list.add(word)

print(symptom_words_list)

filtered_transcript_words = []

for word in transcript_words:
    if word in symptom_words_list:
        filtered_transcript_words.append(word)

print(filtered_transcript_words)

word_pairs = []

for i in range(0, len(filtered_transcript_words)-1):
    word_pairs.append(filtered_transcript_words[i]+" "+filtered_transcript_words[i+1])
    word_pairs.append(filtered_transcript_words[i+1] + " " + filtered_transcript_words[i])

print(word_pairs)

transcript_key_phrases = filtered_transcript_words + word_pairs

print(transcript_key_phrases)

problem_frequency = defaultdict(lambda: 0)

for phrase in transcript_key_phrases:
    if phrase in symptom_database:
        for problem in symptom_database[phrase]:
            problem_frequency[problem] += 1

problem_frequency = sorted([(problem, problem_frequency[problem]) for problem in problem_frequency], key = lambda x: x[1], reverse=True)

print(problem_frequency)

problem_severities = json.load(open("problem_database/problem_severities.json"))

print(problem_severities)

severity = problem_severities[problem_frequency[0][0]]

print(severity)