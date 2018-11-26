from pprint import pprint
import sys


# JSON
# для обмена данными с БД (BSON - для MongoDB)
import json
with open("files/newsafr.json") as datafile:
  json_data = json.load(datafile)
  pprint(json_data)
  print(type(json_data))

with open("files/newsafr2.json", "w") as datafile:
  json.dump(json_data, datafile, ensure_ascii=False, indent=2)