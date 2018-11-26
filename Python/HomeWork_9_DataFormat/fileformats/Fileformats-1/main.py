from pprint import pprint
import json

# with open("files/newsafr.json", encoding="utf-8") as datafile:
#   json_data = json.load(datafile)
# print(type(json_data))

# test_dict = {"test1":"Просто данные"}
# with open("files/newsafr2.json", "w", encoding="utf_8_sig") as datafile:
#   json.dump(test_dict, datafile, ensure_ascii=False)

# КОДИРОВКИ
# encoding="utf_8_sig"
# encoding="utf_8"
# encoding="cp1251"

# import yaml
# with open("files/newsafr.yml") as datafile:
#   yml_data = yaml.load(datafile)
#   print(yml_data)

# with open("files/newsafr2.yml", "w") as datafile:
#   yaml.dump(yml_data, datafile, allow_unicode=True, default_flow_style=True)

# import csv
# csv.register_dialect('customcsv', delimiter=';', quoting=csv.QUOTE_ALL, quotechar='"', escapechar='\\')

# flats_list  = list()
# with open("files/flats.csv") as datafile:
#   csv_data = csv.reader(datafile, delimiter=";")
#   flats_list = list(csv_data)
#   for i, flat in enumerate(csv_data):
#     print(flat)
#     if i == 5:
#       break


# with open("files/flats2.csv", "w") as datafile:
#   datafile_csv = csv.writer(datafile, 'customcsv')
#   datafile_csv.writerow(["test", "test2"])
#   datafile_csv.writerows(flats_list)

import xml.etree.ElementTree as ET
tree = ET.parse("files/newsafr.xml")
titles = []
# что такое корневой элемент xml
root = tree.getroot()
# print(root.tag)
# print(root.attrib)

title = root.find("channel/title")
print(title)
xml_items = root.findall("channel/item")
print(xml_items)
for item in xml_items:
  print(item.attrib["id"])
  print(item.find("title").text)