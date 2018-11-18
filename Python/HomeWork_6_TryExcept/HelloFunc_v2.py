# Задача №1
# Необходимо реализовать пользовательские команды, которые будут выполнять следующие функции:
# p – people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит;
# l– list – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин";
# s – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится;
# a – add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться.
# Внимание: p, s, l, a - это пользовательские команды, а не названия функций. Функции должны иметь выразительное название, передающие её действие.

# kn - key name - вывод данных по ключу

# Задача №2. Дополнительная (не обязательная)
# d – delete – команда, которая спросит номер документа и удалит его из каталога и из перечня полок;
# m – move – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую;
# as – add shelf – команда, которая спросит номер новой полки и добавит ее в перечень;

documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

cmd = ''  # команда


def get_student_name(doc_num):
    '''
    спросить номер документа и вывести имя человека, которому он принадлежит
    '''

    for dict_number in documents:
        for key in dict_number.keys():
            if dict_number[key] == doc_num:
                return dict_number['name']
    return 0


def get_student_docs():
    '''
    вывести список всех документов в формате: Пасспорт "xxxx xxxxxx", "Имя Фамилия"
    '''
    for dict_number in documents:
        print('Документ: {}, номер: {}, Имя: {}'.format(dict_number['type'], dict_number['number'], dict_number['name'],
                                                        '\n'))
    return


def get_docs_shelf(doc_num):
    '''
    спросить номер документа и вывести номер полки, на которой он находится
    '''
    for shelf_number, docs_at_shelf in directories.items():
        for num in shelf_number:
            for doc in docs_at_shelf:
                if doc == doc_num:
                    return num
    return 0


def add_new_student():
    '''
    добавить новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться
    '''
    student_name = input('Введите Имя студента:')
    doc_type = input('Введите тип документа:')
    doc_num = input('Введите номер документа:')
    shelf_num = input('Введите номер полки:')

    if shelf_num in directories.keys():
        documents.append({"type": doc_type, "number": doc_num, "name": student_name})
        directories[shelf_num].append(doc_num)
    else:
        print('Нет полки с таким номеров')
    return


def del_doc(doc_num):
    '''
    спросить номер документа и удалить его из каталога и из перечня полок
    '''
    shelf_num = get_docs_shelf(doc_num)

    if shelf_num != 0:
        directories[shelf_num].remove(doc_num)
        for dict_number, dict_data in enumerate(documents):
            for key in dict_data.keys():
                if dict_data[key] == doc_num:
                    documents.remove(documents[dict_number])
                    print('Записи по номеру документа:', doc_num, 'удалены!')
                    break
    else:
        print('Нет документа с таким номером')
    return


def move_doc(doc_num, new_shelf_num):
    '''
    спросить номер документа и целевую полку и переместить его с текущей полки на целевую
    '''
    shelf_num = get_docs_shelf(doc_num)

    if new_shelf_num in directories.keys():
        if shelf_num != 0:
            directories[shelf_num].remove(doc_num)
            directories[new_shelf_num].append(doc_num)
            print('Документ: {} перемешен на полку №:{}'.format(doc_num, new_shelf_num))
        else:
            print('Нет документа с таким номером')
    else:
        print('Нет полки с таким номеров')


def add_new_shelf(new_shelf_num):
    '''
    спросить номер новой полки и добавить ее в перечень
    '''
    if new_shelf_num in directories.keys():
        print('Полка с номером', new_shelf_num, 'уже существует')
    else:
        directories[new_shelf_num] = []
        print('Добавлена полка с номером:', new_shelf_num)
    return

#-----------------------------------------------------------------------
def get_datas_by_key(key_name):
    '''
    Вывод данных по ключу
    '''

    for dict_number in documents:
        try:
            print(dict_number[key_name])
        except KeyError:
            print('Ошибка ключа')
            print('Перечень возможных ключей:', dict_number.keys())
            break
#-----------------------------------------------------------------------

while cmd != 'q':
    cmd = input('\nВведите команду:')

    if cmd == 'p':
        doc_num = input('Введите номер документа:')
        student_name = get_student_name(doc_num)
        if student_name != 0:
            print('Имя студента:', student_name)
        else:
            print('Нет документа с таким номером')

    elif cmd == 'l':
        get_student_docs()

    elif cmd == 'kn':
        key_name = input('Введите ключ:')
        get_datas_by_key(key_name)

    elif cmd == 's':
        doc_num = input('Введите номер документа:')
        shelf_num = get_docs_shelf(doc_num)
        if shelf_num != 0:
            print('Номер полки:', shelf_num)
        else:
            print('Нет документа с таким номером')

    elif cmd == 'a':
        add_new_student()

    elif cmd == 'd':
        doc_num = input('Введите номер документа:')
        del_doc(doc_num)

    elif cmd == 'm':
        doc_num = input('Введите номер документа:')
        new_shelf_num = input('Переместить на полку:')
        move_doc(doc_num, new_shelf_num)

    elif cmd == 'as':
        new_shelf_num = input('Добавить полку с номером:')
        add_new_shelf(new_shelf_num)

    elif cmd == 'q':
        print('Выход')

    else:
        print('\nСписок комманд:\n')
        print('p – people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит')
        print(
            'l– list – команда, которая выведет список всех документов в формате:passport "2207 876234" "Василий Гупкин"')
        print('s – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится')
        print(
            'a – add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться')
        print('d – delete – команда, которая спросит номер документа и удалит его из каталога и из перечня полок')
        print(
            'm – move – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую')
        print('as – add shelf – команда, которая спросит номер новой полки и добавит ее в перечень')
        print('-' * 25, 'Новая команда', '-' * 25)
        print('kn – key name – команда, которая выводит данные по ключу')
        print('-' * 25, 'Новая команда', '-' * 25)
        print('\nq - quit - завершение работы\n')