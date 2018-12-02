

def read_to_cookbook(filename):
    cook_book = {}
    try:
        with open(filename, encoding = 'utf8') as file:
            for line in file:
                dish = []
                dish_name = line.strip()
                comp_quant = file.readline().strip()
                for num in range(0, int(comp_quant)):
                    component = {}
                    ingridients = file.readline().strip().split('|')
                    component["ingridient_name"] = ingridients[0]
                    component["quantity"] = float(ingridients[1])
                    component["measure"] = ingridients[2]
                    dish.append(component)
                    cook_book[dish_name] = dish
                file.readline().strip()
    except FileNotFoundError:
        print('Нет файла')
    return cook_book

def get_shop_list_by_dishes(dishes, person_count = 1, cook_book = {}):
    shop_list_by_dishes = {}
    for dish in dishes:
        try:
            for component in cook_book[dish]:
                components_list = {}
                component_quantity = component['quantity']
                component_measure = component['measure']
                component_name = component['ingridient_name']
                if component_name in shop_list_by_dishes:
                    component_quantity = component['quantity'] + shop_list_by_dishes[component_name]['quantity']
                components_list['quantity'] = component_quantity * person_count
                components_list['measure'] = component_measure
                shop_list_by_dishes[component_name] = components_list
        except KeyError:
            print('Нет такого блюда:', dish)
            continue
    return shop_list_by_dishes

if __name__ == '__main__':
    cook_book = {}
    cook_book = read_to_cookbook('cook_book.txt')
    dishes = ['Фахитос', 'Омлет', 'Хачапури по-аджарски']
    person_count = 3.0
    shop_list_by_dishes = get_shop_list_by_dishes(dishes, person_count, cook_book)

    print('\nЗаказ:')
    for num, dish in enumerate(dishes):
        print(num + 1, ') ', dish, sep='')
    print('Количество персон:', int(person_count))
    print('\nСписок компонентов для блюд:')
    for component, value in shop_list_by_dishes.items():
        print('{}: {}{}'.format(component, value['quantity'], value['measure']))
