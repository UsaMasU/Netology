cource_euro = 75
day_cost = 10 # euro

trips_count = 3
trip_length_1 = 10 # Turkey
trip_length_2 = 3 # France
trip_length_3 = 5 # Germany

flight_cost = 50
flight_per_trip = 2

print('ЗАДАНИЕ 1: Ассистент путешественника')
print('Курс рубля к 1 евро:',cource_euro)
budget = int(input('Бюджет поездки, евро:'))

trip_cost = (trip_length_1 + trip_length_2 + trip_length_3) * day_cost
trip_cost_rubles =  trip_cost * cource_euro

print('Сумма без перелета:', trip_cost, 'евро','/', trip_cost_rubles, 'рублей')

trip_cost += trips_count * flight_cost * flight_per_trip

print('Полная сумма:',trip_cost,'Евро')

if trip_cost <= budget:
    print('Ок, Зажигаем!!!') # good budget
else:
    print('.....а может лучше автостопом на кубань?') # bad budget

print('\n\nЗАДАНИЕ 2: Линеаризация')
print('Приведение числа X в диапазоне от Xmin до Хmax к виду от 0 до 100%')
x_min = int(input('Xmin = '))
x_max = int(input('Xmax = '))
x = int(input('X = '))

x_proc = (x - x_min)/(x_max - x_min)*100
print('Ответ: число', x ,'равняется', x_proc,'%')