#---------------------------------------------------------------------
# Класс животных
class Animal:
    name = ''
    weight = 0
    weight_max = 0
    weight_min = 0
    metabolism = 1
    sex = ''
    speech = ''
    kind_of_type = ''
    walk_factor = 1

    def __init__(self, name, sex, weight):
        self.name = name
        self.weight = weight
        self.sex = sex
        self.speach = ''
        self.kind_of_type = ''

    def feed(self, feed_value):
        weight_inc = self.weight + feed_value * self.metabolism
        if weight_inc >= self.weight_max:
            print('Cлишком много еды... больше нехочу')
        else:
            print('Покормили! Ням-Ням-Ням')
            self.weight = weight_inc

    def walk(self, walk_hours):
        weight_dec = self.weight - walk_hours * self.walk_factor
        if weight_dec <= self.weight_min:
            print('Гулять.... (( эх сил нет двигаться. Покушать бы...')
        else:
            self.weight = weight_dec
            print('Гулять',walk_hours,'часа! Хорошо на свежем воздухе...))')

    def rename(self, name = ''):
        self.name = name

    def weight_change(self, new_weight):
        self.weight = new_weight

    def talk(self, voice = ''):
        self.speech = voice

    def get_name(self):
        return self.name
#---------------------------------------------------------------------
# Класс млекопитающих
class Mammal(Animal):
    fur_color = ''
    milk_factor = 1

    def __init__(self, name, sex, weight, fur_color):
        super().__init__(name, sex, weight)
        self.fur_color = fur_color

    def milk(self, litres):
        if self.sex == 'ж':
            weight_dec = self.weight - litres * self.milk_factor
            if weight_dec <= self.weight_min:
                print('Молока нет')
            else:
                self.weight = weight_dec
                print('Подоили -',litres,'литров. Наслаждайся молоком')
        else:
            print('Доить?! Это не ко мне')

    def haircut(self):
        print('Постригли. Сшей свитер из моей шерсти и наслаждайся им')
# Класс птиц
class Bird(Animal):
    feather_color = ''
    fly_factor = 2
    eggs_factor = 1.2

    def __init__(self, name, sex, weight, feather_color ):
        super().__init__(name, sex, weight)
        self.feather_color = feather_color

    def fly(self, fly_hours):
        weight_dec = self.weight - fly_hours * self.fly_factor
        if weight_dec <= self.weight_min:
            print('Летать.... (( эх сил нет двигаться. Покушать бы...')
        else:
            self.weight = weight_dec
            print('Я летаю', fly_hours, 'часа! Хорошо на свежем воздухе...))')

    def get_eggs(self, eggs_count):
        if self.sex == 'ж':
            weight_dec = self.weight - eggs_count * self.eggs_factor
            if weight_dec <= self.weight_min:
                print('Пока нет сил высиживать...')
            else:
                self.weight = weight_dec
                print('Я снесла', eggs_count, 'яиц')
        else:
            print('Нести яйца?! Это не ко мне')
#---------------------------------------------------------------------
# Класс коров
class Cow(Mammal):
    def __init__(self, name, sex, weight, fur_color):
        super().__init__(name, sex, weight, fur_color)
        self.speech = 'Мууу'
        self.kind_of_type = 'Корова'
        self.walk_factor = 0.5
        self.metabolism = 1.5
        self.milk_factor = 0.3
        self.weight_max = 400
        self.weight_min = 90

    def haircut(self):
        print('Постричь? Не...  у меня нет столько шерсти для свитера')
# Класс овец
class Sheep(Mammal):
    def __init__(self, name, sex, weight, fur_color):
        super().__init__(name, sex, weight, fur_color)
        self.speech = 'Беееее'
        self.kind_of_type = 'Овца'
        self.walk_factor = 1.5
        self.metabolism = 1.2
        self.weight_max = 90
        self.weight_min = 40

    def milk(self, litres):
        if self.sex == 'ж':
            print('Подоить... хм, мое молоко специфичное на вкус. Лучше делать из него брынзу')
        else:
            print('Доить!? Это не ко мне')
# Класс коз
class Goat(Mammal):
    def __init__(self, name, sex, weight, fur_color):
        super().__init__(name, sex, weight, fur_color)
        self.speech = 'Меееее'
        self.kind_of_type = 'Коза'
        self.walk_factor = 2.5
        self.metabolism = 1.9
        self.milk_factor = 0.8
        self.weight_max = 80
        self.weight_min = 35
# Класс уток
class Duck(Bird):
    def __init__(self, name, sex, weight, feather_color):
        super().__init__(name, sex, weight, feather_color)
        self.speech = 'Кря-Кря'
        self.kind_of_type = 'Утка'
        self.walk_factor = 0.4
        self.fly_factor = 2.1
        self.eggs_factor = 1.5
        self.metabolism = 3.5
        self.weight_max = 5
        self.weight_min = 0.5
# Класс гусей
class Goose(Bird):
    def __init__(self, name, sex, weight, feather_color):
        super().__init__(name, sex, weight, feather_color)
        self.speech = 'Кря'
        self.kind_of_type = 'Гусь'
        self.walk_factor = 0.1
        self.fly_factor = 2.1
        self.eggs_factor = 1.2
        self.metabolism = 3.0
        self.weight_max = 7
        self.weight_min = 0.5
# Класс кур
class Chicken(Bird):
    def __init__(self, name, sex, weight, feather_color):
        super().__init__(name, sex, weight, feather_color)
        self.speech = 'Ко-Ко-Ко-КО'
        self.kind_of_type = 'Курица'
        self.walk_factor = 0.2
        self.fly_factor = 6.5
        self.eggs_factor = 0.3
        self.metabolism = 1.3
        self.weight_max = 8
        self.weight_min = 1.5

    def fly(self, hours):
        print('Летать....эх ( я курица, я не умею летать долго')

#---------------------------------------------------------------------
farm_animals_list = []  # список животных на ферме
sum_weight = 0  # суммарный вес всех животных
max_weight = 0  # вес сомого тяжелого животного
max_weight_name = ''  # имя сомого тяжелого животного
max_weight_animal_type = ''  # вид сомого тяжелого животного

print('\nФерма Дядюшки Джо:')
print('-' * 70)

#---------------------------------------------------------------------
# Создание сущностей и включение их в список животных на ферме

Goose_Gray = Goose('Серый', 'м', 4, 'Серый')
farm_animals_list.append(Goose_Gray)

Goose_White = Goose('Белый', 'м', 3, 'Белый')
farm_animals_list.append(Goose_White)

Cow_Manka = Cow('Манька', 'ж', 200, 'Белый с черными пятнами')
farm_animals_list.append(Cow_Manka)

Sheep_Barash = Sheep('Барашек', 'м', 40, 'Серый')
farm_animals_list.append(Sheep_Barash)

Sheep_Curch = Sheep('Кудрявый', 'м', 45, 'Серый')
farm_animals_list.append(Sheep_Curch)

Chicken_Koko = Chicken('Коко', 'ж', 2, 'Белый')
farm_animals_list.append(Chicken_Koko)

Chicken_Kuka = Chicken('Кукареку', 'ж', 3, 'Рыжий')
farm_animals_list.append(Chicken_Kuka)

Goat_Roga = Goat('Рога', 'ж', 38, 'Белый')
farm_animals_list.append(Goat_Roga)

Goat_Kopyta = Goat('Копыта', 'ж', 35, 'Черный')
farm_animals_list.append(Goat_Kopyta)

Duck_Kryakva = Duck('Кряква', 'ж', 2, 'Серый')
farm_animals_list.append(Duck_Kryakva)

#---------------------------------------------------------------------
# Взаимодействия с животными фермы

print('\n{}: {}, вес: {}кг'.format(Cow_Manka.kind_of_type, Cow_Manka.name, Cow_Manka.weight))
print(Cow_Manka.speech)
Cow_Manka.feed(15)
Cow_Manka.walk(4)
Cow_Manka.milk(10)
Cow_Manka.haircut()
print('{}: {}, вес: {}кг'.format(Cow_Manka.kind_of_type, Cow_Manka.name, Cow_Manka.weight))

print('\n{}: {}, вес: {}кг'.format(Goat_Roga.kind_of_type, Goat_Roga.name, Goat_Roga.weight))
print(Goat_Roga.speech)
Goat_Roga.feed(9)
Goat_Roga.walk(4)
Goat_Roga.milk(6)
print('{}: {}, вес: {}кг'.format(Goat_Roga.kind_of_type, Goat_Roga.name, Goat_Roga.weight))

print('\n{}: {}, вес: {}кг'.format(Goat_Kopyta.kind_of_type, Goat_Kopyta.name, Goat_Kopyta.weight))
print(Goat_Kopyta.speech)
Goat_Kopyta.feed(9)
Goat_Kopyta.walk(4)
Goat_Kopyta.milk(6)
print('{}: {}, вес: {}кг'.format(Goat_Kopyta.kind_of_type, Goat_Kopyta.name, Goat_Kopyta.weight))

print('\n{}: {}, вес: {}кг'.format(Sheep_Barash.kind_of_type, Sheep_Barash.name, Sheep_Barash.weight))
print(Sheep_Barash.speech)
Sheep_Barash.feed(7)
Sheep_Barash.walk(3)
Sheep_Barash.milk(4)
Sheep_Barash.haircut()
print('{}: {}, вес: {}кг'.format(Sheep_Barash.kind_of_type, Sheep_Barash.name, Sheep_Barash.weight))

print('\n{}: {}, вес: {}кг'.format(Sheep_Curch.kind_of_type, Sheep_Curch.name, Sheep_Curch.weight))
print(Sheep_Curch.speech)
Sheep_Curch.feed(6)
Sheep_Curch.walk(4)
Sheep_Curch.milk(4)
Sheep_Curch.haircut()
print('{}: {}, вес: {}кг'.format(Sheep_Curch.kind_of_type, Sheep_Curch.name, Sheep_Curch.weight))

print('\n{}: {}, вес: {}кг'.format(Goose_Gray.kind_of_type, Goose_Gray.name, Goose_Gray.weight))
print(Goose_Gray.speech)
Goose_Gray.feed(0.1)
Goose_Gray.walk(5)
Goose_Gray.get_eggs(3)
print('{}: {}, вес: {}кг'.format(Goose_Gray.kind_of_type, Goose_Gray.name, Goose_Gray.weight))

print('\n{}: {}, вес: {}кг'.format(Goose_White.kind_of_type, Goose_White.name, Goose_White.weight))
print(Goose_White.speech)
Goose_White.feed(0.5)
Goose_White.walk(3)
Goose_White.get_eggs(2)
print('{}: {}, вес: {}кг'.format(Goose_White.kind_of_type, Goose_White.name, Goose_White.weight))

print('\n{}: {}, вес: {}кг'.format(Duck_Kryakva.kind_of_type, Duck_Kryakva.name, Duck_Kryakva.weight))
print(Duck_Kryakva.speech)
Duck_Kryakva.feed(1.6)
Duck_Kryakva.walk(2)
Duck_Kryakva.get_eggs(5)
print('{}: {}, вес: {}кг'.format(Duck_Kryakva.kind_of_type, Duck_Kryakva.name, Duck_Kryakva.weight))

print('\n{}: {}, вес: {}кг'.format(Chicken_Koko.kind_of_type, Chicken_Koko.name, Chicken_Koko.weight))
print(Chicken_Koko.speech)
Chicken_Koko.feed(0.7)
Chicken_Koko.walk(1)
Chicken_Koko.get_eggs(4)
print('{}: {}, вес: {}кг'.format(Chicken_Koko.kind_of_type, Chicken_Koko.name, Chicken_Koko.weight))

print('\n{}: {}, вес: {}кг'.format(Chicken_Kuka.kind_of_type, Chicken_Kuka.name, Chicken_Kuka.weight))
print(Chicken_Kuka.speech)
Chicken_Kuka.feed(0.8)
Chicken_Kuka.walk(3)
Chicken_Kuka.get_eggs(3)
print('{}: {}, вес: {}кг'.format(Chicken_Kuka.kind_of_type, Chicken_Kuka.name, Chicken_Kuka.weight))

print('-' * 70)

#---------------------------------------------------------------------
# Подсчет общего веса животных фермы
# Пойск животного с самым большим весом

for animal in farm_animals_list:
    sum_weight += animal.weight
    if animal.weight > max_weight:
        max_weight = animal.weight
        max_weight_name = animal.name
        max_weight_animal_type = animal.kind_of_type

print('\nСуммарный вес животных на ферме Дядюшки Джо равен {:.{prec}f}кг'.format(sum_weight, prec = 3))
print('Самым большим весом = {:.{prec}f}кг'.format(max_weight, prec = 3),'обладает {} по имени: {}'.format(max_weight_animal_type, max_weight_name))