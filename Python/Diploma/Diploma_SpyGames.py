import requests
import json
import time

APP_ID = 6775694  # ID приложения VK
AUTH_URL = 'https://oauth.vk.com/authorize?'  # сылка для авторизации
VK_ID_URL = 'https://vk.com/id'  # шаблон для ссылки на профиль
M_URL = 'https://api.vk.com/method/'  # ссылка для использования API
M_NAME = ''  # имя вызываемого метода

# данные для запроса токена
auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'response_type': 'token',
    'scope': 'friends,status',
    'v': '5.52'
}
# активный токен
# token = '8f9e5ab49db2fd32ab5d8ca59e548b3bec5aa0c4a66a2b91abebd683a228c1024ba2217a5efb226e6ac33'
# token = '33dada42f424ac65e363704ad2595f645d926cf8f5879ab8eab648f856c83e3b4ea10dfb4758392cbe44d'
token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
ver = '5.92'  # версия API


def check_token():
    """
    функция проверки актуальности токена
    """
    response = {}
    conn_attempts = 0  # счетчик попыток соедининеня
    while conn_attempts != 5:  # 5 попыток
        try:
            response = requests.get(M_URL + 'users.get', {'user_ids': '1', 'access_token': token, 'v': ver})
            break
        except requests.exceptions.Timeout:
            print('Timeout! Повтор попытки соединения...')
            conn_attempts += 1
            time.sleep(1.0)  # пауза между попытками
        except requests.exceptions.RequestException:
            print('Error Request! Повтор попытки соединения...')
            conn_attempts += 1
            time.sleep(1.0)   # пауза между попытками
        if conn_attempts == 5:
            print('Ошибка соединения!')
            exit(1)  # завершение работы
    conn_state = response.json()
    for state, val_state in conn_state.items():
        if state == 'error':
            if(val_state['error_code']) == 5:
                return 0
    return 1


class WorkTimer:
    """
    менеджер контекста для оценки времени выполнения
    """
    time_start = 0
    time_finish = 0
    time_work = 0

    def __init__(self, name):
        self.time_start = 0
        self.time_finish = 0
        self.time_work = 0
        self.name = name

    def __enter__(self):
        self.time_start = time.time()
        time_in_format = time.strftime("%H.%M.%S", time.localtime())  # "%Y-%m-%d-%H.%M.%S"
        print(self.name, ': старт выполнения: ', time_in_format, sep='')

    def __exit__(self, time_start, time_finish, time_work):
        self.time_finish = time.time()
        time_in_format = time.strftime("%H.%M.%S", time.localtime())  # "%Y-%m-%d-%H.%M.%S"
        print(self.name, ': стоп выполнения: ', time_in_format, sep='')
        self.time_work = self.time_finish - self.time_start
        print(self.name, ': продолжительность: {:.{prec}f} sec'.format(self.time_work, prec=3), sep='')


class User:
    """
    класс пользователь VK
    """
    global token, ver  # глобальные данные используемые во всех запросах
    obj_name = ''  # имя экземпляра
    uid = ''  # ID
    link_url = ''  # ссылка на профиль
    profile = {  # профиль
        'id': '',  # ID
        'first_name': '',  # имя
        'last_name': '',  # фамилия
        'nickname': '',  # ник
        'bdate': '',  # дата рождения
        'sex': '',  # пол
        'status': ''  # статус
    }
    friends = {}  # список друзей
    groups = {}  # список групп
    groups_data = {}  # подробные данные групп

    def __init__(self, settings):
        #  если имя в параметрах пропущено то задаем пустое имя экземпляру
        try:
            settings['obj_name']
        except KeyError:
            settings['obj_name'] = ''
        finally:
            self.obj_name = settings['obj_name']
            # инициализируем профиль
            self.profile = {
                'id': '',
                'first_name': '',
                'last_name': '',
                'nickname': '',
                'bdate': '',
                'sex': '',
                'status': ''
            }
            self.friends = {}
            self.groups = {}
        # если переданы данные профиля то заполняем ими профиль
        try:
            if settings['profile_data'] != '':
                self.set_user(settings['profile_data'])
        except KeyError:
            pass
        # если передан id то запрашиваем профиль у VK
        try:
            if settings['uid'] != '':
                self.get_user(settings['uid'])
        except KeyError:
            pass

    def __str__(self):
        return str(self.link_url)  # передача ссылки на профиль

    def __and__(self, other):
        """
        вызов &
        """
        response = self.get_cross_friends(self.uid, other.uid)  # запрос общих друзей
        return response

    def get_user(self, uid):
        """
        запрос даннх профиля пользователя от VK
        """
        params = {
            'user_ids': uid,
            'fields': 'nickname,name,sex,bdate,status',
            'access_token': token,
            'v': ver
        }
        response = self.get_data('users.get', params)  # запрос данных VK
        user_data = response.json()
        # полученные данные в цикле переписываем в профиль
        for key in self.profile.keys():
            try:
                self.profile[key] = user_data['response'][0][key]
            except KeyError:
                pass
        self.uid = str(user_data['response'][0]['id'])  # записываем ID
        self.link_url = VK_ID_URL + self.uid  # формируем ссылку на профиль VK
        return user_data['response']

    def set_user(self, user_data):
        """
        заполнение профиля данными
        """
        # формируем записываемые данные в зависимости от типа вызова метода
        if 'profile_data' in user_data:
            set_user_data = user_data['profile_data']
        else:
            set_user_data = user_data
        print(set_user_data)
        # в цикле заполняем профиль
        for key in self.profile.keys():
            try:
                self.profile[key] = set_user_data[key]
            except KeyError:
                pass
        self.uid = str(set_user_data['id'])  # записываем ID
        self.link_url = VK_ID_URL + self.uid  # формируем ссылку на профиль VK

    def get_friends_list(self):
        """
        запрос списка друзей пользователя VK
        """
        params = {
            'user_id': self.uid,
            'access_token': token,
            'v': ver
        }
        # запрос данных VK
        response = self.get_data('friends.get', params)
        friends_data = response.json()
        self.friends = friends_data['response']
        return self.friends

    def get_groups_list(self):
        """
        запрос списка групп пользователя VK
        """
        params = {
            'user_id': self.uid,
            'extended': '0',
            'access_token': token,
            'v': ver
        }
        response = self.get_data('groups.get', params)  # запрос данных VK
        groups_data = response.json()
        self.groups = groups_data['response']
        return self.groups

    def get_groups_data(self):
        """
        запрос подробных данных групп пользователя VK
        """
        params = {
            'user_id': self.uid,
            'extended': '1',
            'fields': 'members_count',
            'access_token': token,
            'v': ver
        }
        response = self.get_data('groups.get', params)  # запрос данных VK
        groups_data = response.json()
        self.groups_data = groups_data['response']
        return self.groups_data

    def get_cross_friends_list(self, src_uid, tar_uid):
        """
        запрос списка общих друзей в VK
        """
        params = {
            'source_uid': src_uid,
            'target_uid': tar_uid,
            'access_token': token,
            'v': ver
            }
        response = self.get_data('friends.getMutual', params)  # запрос данных VK
        users_data = response.json()
        return users_data['response']

    def get_cross_friends(self, src_uid, tar_uid):
        """
        формирование экземпляров из списка общих друзей
        """
        cross_friends_obj = []
        cross_friends_list = self.get_cross_friends_list(src_uid, tar_uid)
        for i, friend in enumerate(cross_friends_list):
            print(i + 1, ': id ', friend, sep='')
            # создания экземпляра и запись его в список экземпляров
            cross_friends_obj.append(User({'uid': friend}))
        return cross_friends_obj

    def get_cross_groups(self, start_group_num=0, stop_group_num=0):
        """
        поиск общих групп пользователя и друзей
        """
        #  Настройка параметров границ анализа количества групп пользоателя
        if start_group_num != 0 and stop_group_num == 0:
            stop_group_num = start_group_num
        if start_group_num == 0 and stop_group_num == 0:
            start_group_num = 1
            stop_group_num = self.groups['count']
        if stop_group_num < start_group_num:
            stop_group_num = self.groups['count']
        if start_group_num > stop_group_num:
            start_group_num = 1

        print('\nАнализ групп пользователя:')
        print('Группы с {} по {}:'.format(start_group_num, stop_group_num))

        offset = 0  # начальное смещение
        count = 24  # Количество запросов внутри execute
        cross_groups = []  # список пересекающихся групп
        cross_friends = []  # список количества пересечений
        friends_count = 0  # счечик по друзьям

        # цикл перебора групп друзей
        for num_group, group in enumerate(self.groups['items']):
            #  если порядковый номер группы вне аналитического деапазона, то пропускаем
            if num_group+1 < start_group_num or num_group+1 > stop_group_num:
                continue
            #  если перебрали всех друзей, то обнуляем счетчик и смещение
            if friends_count == self.friends['count']:
                friends_count = 0
                offset = 0
            #  цикл перебора друзей с поисклм пересечений в группах.
            #  выполняется на стороне VK методом execute.
            #  1) запрос порции для анализа друзей (24 друга)
            #  2) далее анализ этих 24 групп
            while friends_count < self.friends['count']:
                # параметры для запроса execute
                params = {
                    'access_token': token,
                    'v': ver,
                    'code': (
                            "var id = " + str(self.uid) + ";"
                            "var offset = " + str(offset) + ";"
                            "var count = " + str(count) + ";"
                            "var group_id = " + str(group) + ";"
                            "var friends_count = " + str(friends_count) + ";"     
                            "var session_count = 0;"
                            "var order = "'"name"'";"
                            "var fields = "'"nickname"'";"
                            "var user = null;"
                            "var friends = null;"
                            "var groups = null;"
                            "var groups_items = null;"
                            "var check_id = 0;"
                            "var group_match = 0;"

                            "friends = API.friends.get({""user_id"": id, ""offset"": offset, ""count"": count});"
                            "var friend_counter = friends.items.length;"
                      
                            "while (friend_counter != 0) {"
                                "groups =  API.groups.get({""user_id"": friends.items[friend_counter],"
                                                                          " ""extended"": 1});"
                                "groups_items = groups.items;"
                                
                                "check_id = groups_items@.id.indexOf(group_id);"                    
                                "if (check_id != -1) {"
                                    "group_match = group_match + 1;"
                                 "};"
                              
                                "friend_counter = friend_counter - 1;"
                                "session_count = session_count + 1;"
                                "friends_count = friends_count + 1;"
                            "};"
                            "return [group_id, session_count, friends_count, group_match];"
                    )

                }
                response = self.get_data('execute', params)  # вызов execute

                try:
                    exec_data = response.json()
                    print(num_group+1, ') ID: ', exec_data['response'][0],
                          '; проверено друзей: ', exec_data['response'][2], sep='')

                    offset = offset + exec_data['response'][1]  # увеличение смещения
                    friends_count = exec_data['response'][2]  # изменение счетчика друзей пользователя

                    # если обнаружено пересечение группы друга с группой пользовтеля
                    if exec_data['response'][3] > 0:
                        cross_groups.append(exec_data['response'][0])  # запись группы пересечения
                        cross_friends.append(exec_data['response'][3])  # запись количесва друзей в этой группе
                        # friends_count = self.friends['count']  # прекращаем дальнейший пойск по этой группе
                        print('Обнаружена общая группа!')
                except KeyError:
                    print('Error key JSON')
        return cross_groups, cross_friends

    def show_cross_groups(self, cross_groups, cross_friends, max_friends=1):
        """
        подготовка данных по общим группам и количеству друзей в них
        но не более чем max_friends
        """
        cross_groups_friends = {}  # общие группы пользователя и друзей
        filter_cross_groups = {}  # общие группы пользователя и друзей, где друзей < max_friends
        for num, group in enumerate(cross_groups):
            try:
                cross_groups_friends[group] += cross_friends[num]
            except KeyError:
                cross_groups_friends[group] = cross_friends[num]

        for group in cross_groups_friends:
            if cross_groups_friends[group] <= max_friends:
                filter_cross_groups[group] = cross_groups_friends[group]

        return filter_cross_groups

    def get_data(self, method_name='', params=dict, delay_time=0.0):
        """
        выполнение запроса к VK API
        """
        time.sleep(delay_time)  # пауза чтобы VK не заблокировал соединение
        print('*')
        response = {}
        conn_attempts = 0  # счетчик попыток соединения
        while conn_attempts != 5:  # 5 попыток
            try:
                response = requests.get(M_URL + method_name, params)  # строка запроса данных VK
                break
            except requests.exceptions.Timeout:
                print('Timeout! Повтор попытки соединения...')
                conn_attempts += 1
                time.sleep(1.0)  # пауза между попытками
            except requests.exceptions.RequestException:
                print('Error Request! Повтор попытки соединения...')
                conn_attempts += 1
                time.sleep(1.0)  # пауза между попытками
            if conn_attempts == 5:
                print('Ошибка соединения!')
                exit(1)  # завершение работы
        return response


if __name__ == '__main__':
    # Проверка токена
    token_true = check_token()
    if token_true == 0:
        print('Необходим новый токен')
        exit(1)

    with WorkTimer('Поиск уникальных групп'):
        # создание экземпляра пользователя
        User_One = User({'uid': 'eshmargunov'})  # eshmargunov
        print(User_One.profile['first_name'], User_One.profile['last_name'])
        print(User_One)  # ссылка на профиль VK
        User_One.get_groups_list()  # запрос списка групп
        User_One.get_groups_data()  # запрос подробных данных групп
        User_One.get_friends_list()  # запрос списка друзей

        print('Количество друзей:', User_One.friends['count'])
        print('Количество групп:', User_One.groups['count'])
        for num, group in enumerate(User_One.groups['items']):
            print(num+1, ') ', group, sep='')

        # формирование множества групп пользователя
        user_group_list = set()
        for group in User_One.groups['items']:
            user_group_list.add(group)

        # поиск общих с другими пользователями групп
        cross_groups, cross_friends = User_One.get_cross_groups()

        max_friends = 3  # максимальное допустимое количкство друзей в общих группах
        print('\nОбщие группы с количеством друзей не более:', max_friends)
        cross_groups_friends = User_One.show_cross_groups(cross_groups, cross_friends, max_friends)

        for num, cross_group in enumerate(cross_groups_friends.items()):
            print(num+1, ') ', 'ID: ', cross_group[0], '; друзей: ', cross_group[1], sep='')

        # формирование множества пересекающихся групп пользователя и групп его друзей
        cross_groups_list = set()
        for group in cross_groups:
            cross_groups_list.add(group)

        #  формирование множества уникальных групп пользователя
        user_unique_list = set()
        user_unique_list = user_group_list.difference(cross_groups_list)

        #  формирование данных для записи в JSON-файл
        group_data_json = []  # список уникальных групп пользователя
        for uniquie_group in user_unique_list:
            for data in User_One.groups_data['items']:
                group_data = {}  # словарь данных уникальной группы пользователя
                if uniquie_group == data['id']:
                    try:  # записываем необходиые данные уникальных групп
                        group_data['gid'] = data['id']
                        group_data['name'] = data['name']
                        group_data['members_count'] = data['members_count']
                    except KeyError:  # если попытка записи не удалась
                        pass  # пропускаем группу
                    finally:
                        group_data_json.append(group_data)  # добавление в список уникальных групп

        # сохранение уникальных групп пользователя в JSON-файл
        with open("groups.json", "w", encoding="utf-8") as file:
            json.dump(group_data_json, file)

    # открываем созданный JSON-файл и считываем сохраненные группы
    with open("groups.json", encoding="utf-8") as file_read:
        json_data = json.load(file_read)
    print('\nУникальные группы пользователя:')
    for group in json_data:
        print(group)