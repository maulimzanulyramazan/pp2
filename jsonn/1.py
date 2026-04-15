import json
data_json = input()
data_py = json.loads(data_json)
print(data_py["age"])