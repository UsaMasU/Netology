print('Task 1:\n')

budget = 20000

countries = {
    'Thailand': {'country_sea': True, 'country_schengen': False, 'exchange_rate': 2, 'temperature': 28,
                 'living_cost': 900},
    'Germany': {'country_sea': True, 'country_schengen': True, 'exchange_rate': 74, 'temperature': 10,
                'living_cost': 50},
    'Poland': {'country_sea': True, 'country_schengen': True, 'exchange_rate': 18, 'temperature': 8,
               'living_cost': 150},
    'Russia': {'country_sea': True, 'country_schengen': False, 'exchange_rate': 1, 'temperature': 5,
               'living_cost': 2000}
}

countries['France'] = {'country_sea': True, 'country_schengen': True, 'exchange_rate': 5, 'temperature': 21,
                       'living_cost': 50}
countries['Spain'] = {'country_sea': True, 'country_schengen': True,
                      'exchange_rate': 11, 'temperature': 27, 'living_cost': 150}
countries['Austria'] = {'country_sea': False, 'country_schengen': True, 'exchange_rate': 7, 'temperature': 18,
                        'living_cost': 90}

countries_with_schengen = set()
countries_with_sea = set()
countries_for_visit = set()

for country, conditions in countries.items():
    if (conditions['country_sea'] == True and countries[country]['temperature'] >= 20 and (
            countries[country]['living_cost'] * 10 * countries[country]['exchange_rate']) <= budget):
        countries_with_schengen.add(country)
    if (conditions['country_schengen'] == True and (
            countries[country]['living_cost'] * 7 * countries[country]['exchange_rate']) <= budget):
        countries_with_sea.add(country)

countries_for_visit = (countries_with_schengen | countries_with_sea)

print('The list of countries for visit:')
for country in countries_for_visit:
    print(country)

# ----------
print('\n\nЗАДАНИЕ 2:\n')

cook_book = {
    'салат':
        [
            ['картофель', 100],
            ['морковь ', 50],
            ['огурцы', 50],
            ['горошек', 30],
            ['майонез', 70],
        ],
    'пицца':
        [
            ['сыр', 50],
            ['томаты', 50],
            ['тесто', 100],
            ['бекон', 30],
            ['колбаса', 30],
        ],
    'фруктовый десерт':
        [
            ['хурма', 60],
            ['киви', 60],
            ['творог', 60],
            ['сахар', 10],
            ['мед', 50],
        ]
}

person = 3
specification = {}
pos_in_spec = 0

print('Количество персон:', person)
print('\nСпецификация продуктов:')

for indigrients in cook_book.values():
    for component in indigrients:
        pos_in_spec += 1
        comp_name = component[0]
        comp_weight = component[1] * person
        specification[comp_name] = comp_weight
        print(pos_in_spec, ') ', comp_name, ': ', specification[comp_name], 'гр.', sep='')

