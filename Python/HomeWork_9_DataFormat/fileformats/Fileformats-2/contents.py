from pprint import pprint

# CSV
# конвертируется в Excel, самый распространенный формат для публикации данных
import csv
with open('files/flats.csv', newline='') as csvfile:
	flats_csv = csv.reader(csvfile, delimiter=';')
	flats_list = list(flats_csv)
print(flats_list[:5])

csv.register_dialect('customcsv', delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"', escapechar='\\')
with open('files/flats2.csv', "w", encoding='utf-8', newline='') as f:
    csvfile = csv.writer(f, 'customcsv')
    csvfile.writerows(flats_list[:5])

# JSON
# для обмена данными с БД (BSON - для MongoDB)
# import json
# with open("files/newsafr.json") as datafile:
#   json_data = json.load(datafile)
#   pprint(json_data)
#   print(type(json_data))

# with open("files/newsafr2.json", "w") as datafile:
#   json.dump(json_data, datafile, ensure_ascii=False, indent=2)

# YAML
# import yaml
# with open("files/newsafr.yml") as datafile:
#   yaml_data = yaml.load(datafile)
#   pprint(yaml_data)

# with open("files/newsafr2.yml", "w") as datafile:
#   yaml.dump(json_data, datafile, allow_unicode=True, default_flow_style=False)



# XML
# наследие Microsoft
# чтение XML
# import xml.etree.ElementTree as ET
# tree = ET.parse("files/newsafr.xml")
# # что такое корневой элемент xml
# root = tree.getroot()
# # теги и атрибуты
# print(root.tag)
# print(root.attrib)
# # поиск в XML
# xml_title = root.find("channel/title")
# xml_items = tree.findall("channel/item")
# print(len(xml_items))
# # ... и почему не работает вот так
# xml_items = tree.findall("rss/channel/item")
# # как работать с элементами XML DOM
# # https://ru.wikipedia.org/wiki/Document_Object_Model
# # получить значение элемента - text
# for item in xml_items:
#   title = item.find("title")
#   print(title.text)