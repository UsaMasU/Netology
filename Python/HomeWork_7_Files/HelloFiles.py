cook_book = {}

def read_to_cookbook(filename = '', cook_book = {}):
    with open(filename, encoding='utf8') as file:
        while(True):
            dish = []
            dish_name = file.readline().strip()
            if dish_name == '$':
                break
            comp_quant = file.readline().strip()
            for num in range(1, int(comp_quant) + 1):
                component = {}
                ingridients = file.readline().split('|')
                component["ingridient_name"] = ingridients[0]
                component["quantity"] = float(ingridients[1])
                component["measure"] = ingridients[2]
                dish.append(component)
                cook_book[dish_name] = dish
            space_line = file.readline()

def get_shop_list_by_dishes(dishes, person_count):
    shop_list_by_dishes = {}
    ig_list = {}
    for dish in dishes:
        for ingridient in dish:
            ig_list['measure'] = ingridient['measure']
            quantity_with_person_count = ig_list['quantity'] = ingridient['quantity'] * person_count
            ig_list['quantity'] = quantity_with_person_count
            if shop_list_by_dishes.get(ingridient['ingridient_name']):
                get_ingridient = shop_list[ingridient['ingridient_name']]
                get_quantity = get_ingridient['quantity']
                ig_list['quantity'] += get_quantity
            shop_list_by_dishes[ingridient['ingridient_name']] = ig_list
    return shop_list_by_dishes


read_to_cookbook('cook_book.txt', cook_book)

dishes = [cook_book['Фахитос'],cook_book['Утка по-пекински']]
shop_list = {}
person_count = 2.0

shop_list = get_shop_list_by_dishes(dishes, person_count)
print(shop_list)