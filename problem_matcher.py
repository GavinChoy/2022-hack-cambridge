import json
from collections import defaultdict


# load dictionary of problems and their associated list of symptoms
original_database_file = open("problem_database.json")
symptoms_for_each_problem = json.load(original_database_file)["problems"]

# transform the original dictionary to allow efficient search of symptoms
# dictionary: {symptom:[list of potential problems]}
# dictionary: {problem:severity}
# dictionary: {problem:action}
problems_for_each_symptom = defaultdict(lambda: set())
severity_for_each_problem = {}
action_for_each_problem= {}

for problem in symptoms_for_each_problem:
    severity_for_each_problem[problem["problem"]] = problem["severity"]
    action_for_each_problem[problem["problem"]] = problem["action"]
    for symptom in problem["symptoms"]:
        problems_for_each_symptom[symptom].add(problem["problem"])

        # generate plural forms for the symptoms
        # improve symptom and transcript matching
        words = symptom.split()
        if len(words) > 1:
            problems_for_each_symptom[words[0] + "s " + words[1]].add(problem["problem"])
            problems_for_each_symptom[words[0] + " " + words[1] + "s"].add(problem["problem"])
            problems_for_each_symptom[words[0] + "s " + words[1] + "s"].add(problem["problem"])

# a set was used to remove duplicate potential problems for each symptom
for symptom in problems_for_each_symptom:
    problems_for_each_symptom[symptom] = list(problems_for_each_symptom[symptom])


def determine_problems(monitor_output, lang="same"):
    """
    PARAMETERS:
        monitor_output: the output from the monitor which is a dictionary of the transcript details
        lang="same": for English originals, set otherwise for patients speaking in another language

    OUTPUT:
        dictionary of the form {'patient_number': patient number/ID, 'timestamp': timestamp of transcript, 'severity': overall severity score of patient request, 'most_likely_problems': [potential problem 1, potential problem 2, etc...], 'transcript': original transcript text, 'action': [(problem 1, recommended action for problem 1), (problem 2, recommended action for problem 2), etc...]}
    """

    # form a list of words and their Deepgram confidences
    words_and_confidences = []

    if lang == "same":
        for word_confidence in monitor_output["word_confidences"]:
            words_and_confidences.append((word_confidence["word"], word_confidence["confidence"]))
    else:
        for word in monitor_output["translated"].split(" "):
            words_and_confidences.append((word, monitor_output["total_confidence"]))

    # form a list of words found in the symptoms database
    symptom_database = problems_for_each_symptom
    symptom_words_list = set()
    for symptom in symptom_database:
        for word in symptom.split():
            symptom_words_list.add(word)

    # filter transcript words to only include those found in the symptoms database
    filtered_words_confidences = []
    for word_and_confidence in words_and_confidences:
        if word_and_confidence[0] in symptom_words_list:
            filtered_words_confidences.append(word_and_confidence)

    # form pairs of words because some of symptoms have two words
    word_and_confidence_pairs = []
    for i in range(0, len(filtered_words_confidences) - 1):
        mean_confidence = 0.5 * (filtered_words_confidences[i][1] + filtered_words_confidences[i + 1][1])
        word_and_confidence_pairs.append((filtered_words_confidences[i][0] + " " + filtered_words_confidences[i + 1][0], mean_confidence))
        word_and_confidence_pairs.append((filtered_words_confidences[i + 1][0] + " " + filtered_words_confidences[i][0], mean_confidence))
    transcript_key_phrases = filtered_words_confidences + word_and_confidence_pairs

    # find potential problems
    # record the frequency of symptoms matched for the potential problems
    # record the severity rating of the potential problems based on their frequency and problem severity
    problem_frequencies = defaultdict(lambda: 0)
    problem_severity_weights = defaultdict(lambda: 0.0)
    for phrase in transcript_key_phrases:
        if phrase[0] in symptom_database:
            for problem in symptom_database[phrase[0]]:
                problem_frequencies[problem] += 1
                # increase problem severity weight by confidence multiplied by the severity of the problem
                problem_severity_weights[problem] += phrase[1] * severity_for_each_problem[problem]
    # sort problems by number of symptoms matched then sort by problem severity
    problem_frequencies = sorted(sorted([(problem, problem_frequencies[problem]) for problem in problem_frequencies], key=lambda x: severity_for_each_problem[x[0]], reverse=True),
                               key=lambda x: x[1], reverse=True)

    if problem_frequencies:
        total_severity_weight = 0
        total_frequency = 0
        # find weighted average of all potential problems
        for (problem, problem_frequency) in problem_frequencies:
            total_severity_weight += problem_severity_weights[problem]
            total_frequency += problem_frequency
        severity = total_severity_weight / total_frequency

        actions=[]
        for (problem, freq) in problem_frequencies:
            action=action_for_each_problem[problem]
            actions.append((problem, action))

        potential_problems = [problem for (problem, problem_frequency) in problem_frequencies]

        return {"patient_number":monitor_output["patient_number"],
                "timestamp":monitor_output["timestamp"],
                "severity": severity,
                "most_likely_problems":potential_problems,
                "transcript": monitor_output["transcript"],
                "action":actions}
    else:
        return {"patient_number":monitor_output["patient_number"],
                "timestamp":monitor_output["timestamp"],
                "severity": 0,
                "most_likely_problems":[],
                "transcript": monitor_output["transcript"],
                "action":[("None", "None")]
                }