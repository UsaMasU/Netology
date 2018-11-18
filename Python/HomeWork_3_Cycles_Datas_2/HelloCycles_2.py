import csv

flats_list = list()

with open('output.csv', newline='') as csvfile:
	flats_csv = csv.reader(csvfile, delimiter=';')
	flats_list = list(flats_csv)

#можете посмотреть содержимое файла с квартирами через print, можете - на вкладке output.csv
#print (flats_list)

#print(flats_list[0],'\n')

#TODO 1:
# 1) Напишите цикл, который проходит по всем квартирам, и показывает только новостройки
#и их порядковые номера в файле.
# 2) добавьте в код подсчет количества новостроек

print('\n---1----------\n')
print('Новостройки:\n')

count_new_build = 0
for num, flat in enumerate(flats_list):
  if "новостройка" in flat:
    print("{}:\n{}".format(num, flat),'\n')
    count_new_build += 1
print('количество новостроек:', count_new_build)

#TODO 2:
# 1) Сделайте описание квартиры в виде словаря, а не списка. Используйте следующие поля из файла output.csv: ID, Количество комнат;Новостройка/вторичка, Цена (руб).

print('\n---2.1--------\n')
flat_number = 100

flat_info = {"id":flats_list[flat_number][0], "rooms":flats_list[flat_number][1], "type":flats_list[flat_number][2], "price":flats_list[flat_number][11]}

print('\n#: {}\nid: {}\nrooms: {}\ntype: {}\nprice: {}руб.\n'.format(flat_number, flat_info['id'], flat_info['rooms'], flat_info['type'], flat_info['price'] ))

# 2) Измените код, который создавал словарь для поиска квартир по метро так, чтобы значением словаря был не список ID квартир, а список описаний квартир в виде словаря, который вы сделали в п.1

print('\n---2.2--------\n')

flats_list.pop(0)

subway_dict = {}
for flat in flats_list:
  subway = flat[3].replace("м.", "")
  if flat[3]=='':
    continue
  if subway not in subway_dict.keys():
    subway_dict[subway] = list()
  subway_dict[subway].append(flat[12])

for flat, flats_info in subway_dict.items():
  print('-' * 5,flat,'-' * 5,'\n')
  for flat_num, data in enumerate(flats_info):
    print(flat_num + 1,') Описание кваритры:\n', data, '\n', sep = '')

# 3) Самостоятельно напишите код, который подсчитывает и выводит, сколько квартир нашлось у каждого метро.

print('\n---3----------\n')
print('Количество квартир возле станций метро:\n')

for subway_station, flats_near_subway  in subway_dict.items():
  print(subway_station, ': ', len(flats_near_subway), sep = '')