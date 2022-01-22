import json
from collections import defaultdict

original_database_file = open("problem_database.json")

symptoms_for_each_problem = json.load(original_database_file)["problems"]

problems_for_each_symptom = defaultdict(lambda: set())
severity_for_each_problem = {}

for problem in symptoms_for_each_problem:
    severity_for_each_problem[problem["problem"]] = problem["severity"]
    for symptom in problem["symptoms"]:
        problems_for_each_symptom[symptom].add(problem["problem"])


def convert_set_to_list(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

with open("symptom_database.json", "w") as symptom_database:
    json.dump(problems_for_each_symptom, symptom_database, default=convert_set_to_list)

with open("problem_severities.json", "w") as severity_database:
    json.dump(severity_for_each_problem, severity_database)