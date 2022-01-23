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

        words = symptom.split()

        if len(words) > 1:
            problems_for_each_symptom[words[0] + "s " + words[1]].add(problem["problem"])
            problems_for_each_symptom[words[0] + " " + words[1] + "s"].add(problem["problem"])
            problems_for_each_symptom[words[0] + "s " + words[1] + "s"].add(problem["problem"])

for symptom in problems_for_each_symptom:
    problems_for_each_symptom[symptom] = list(problems_for_each_symptom[symptom])


def determine_problems(monitor_output, lang="same"):
    words_and_confidences = []

    if lang == "same":
        for word_confidence in monitor_output["word_confidences"]:
            words_and_confidences.append((word_confidence["word"], word_confidence["confidence"]))
    else:
        for word in monitor_output["translated"].split(" "):
            words_and_confidences.append((word, monitor_output["total_confidence"]))

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
        return {"patient_number":monitor_output["patient_number"],
                "timestamp":monitor_output["timestamp"],
                "severity": 0,
                "most_likely_problems":[("None", 1)],
                "transcript": monitor_output["transcript"],
                "action":[("None", "None")]
                }
