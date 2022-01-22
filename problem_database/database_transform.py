import json
from collections import defaultdict

original_database_file = open("problem_database.json")

symptoms_for_each_problem = json.load(original_database_file)["problems"]

problems_for_each_symptom = defaultdict(lambda: set())

for problem in symptoms_for_each_problem:
    for symptom in problem["symptoms"]:
        problems_for_each_symptom[symptom].add(problem["problem"])


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

with open("symptom_database.json", "w") as symptom_database:
    json.dump(problems_for_each_symptom, symptom_database, default=set_default)