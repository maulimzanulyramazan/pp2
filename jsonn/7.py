import json
students_json = '''
[
    {"name": "Ali", "grades": [90, 80, 85]},
    {"name": "Madi", "grades": [70, 75, 80]},
    {"name": "Amina", "grades": [95, 92, 96]}
]
'''
data = json.loads(students_json)
a = {}
for i in range(3):
    a[data[i]["name"]] = sum(data[i]["grades"]) / 3
for key, val in sorted(a.items(), key = lambda x: x[1]):
    print(f"{key}: {val:.2f}")