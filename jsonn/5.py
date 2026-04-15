import json
students_json = '''
[
    {"name": "Ali", "grade": 90},
    {"name": "Madi", "grade": 85},
    {"name": "Aruzhan", "grade": 95}
]
'''
data = json.loads(students_json)
for i in range(3):
    print(data[i]["name"], data[i]["grade"])