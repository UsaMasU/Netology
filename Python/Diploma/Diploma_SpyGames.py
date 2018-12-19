from pprint import pprint
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
#token = '9627011e638fd171aa683a0f3b507e10b93b7b1662d32b71d3d1f9e54681bee6b921ab2681bcf815c11c6'
token = '925b144b540d411baa0f5c43ea6fbce1942a7e597df7348818bb12a7d248018b9ee2c6bbcbb4db3671c74'
ver = '5.92'  # версия API

# функция проверки актуальности токена
def check_token():
    response = requests.get(M_URL + 'users.get', {'user_ids': '1', 'access_token': token, 'v': ver})
    conn_state = response.json()
    for state, val_state in conn_state.items():
        if state == 'error':
            if(val_state['error_code']) == 5:
                return 0
    return 1

class WorkTimer:
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
        print(self.name, ': Start operation time: ', time_in_format, sep='')

    def __exit__(self, time_start, time_finish, time_work):
        self.time_finish = time.time()
        time_in_format = time.strftime("%H.%M.%S", time.localtime())  # "%Y-%m-%d-%H.%M.%S"
        print(self.name, ': Finish operation time: ', time_in_format, sep='')
        self.time_work = self.time_finish - self.time_start
        print(self.name, ': Operation lasts: {:.{prec}f} sec'.format(self.time_work, prec = 3), sep = '')

# класс пользователь VK
class User:
    global token, ver  # глобальные данные используемые во всех запросах
    obj_name = ''  # имя экземпляра
    uid = '' # ID
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
    friends = {}
    groups = {}

    # инициализация обьекта
    def __init__(self, settings={}):  # {'obj_name': '', 'uid': '', 'profile_data': ''}
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

    # по умолчанию передача ссылки на профиль
    def __str__(self):
        return str(self.link_url)

    # вызов &
    def __and__(self, other):
        # запрос общих друзей
        response = self.get_cross_friends(self.uid, other.uid)
        return response

    # запрос даннх профиля пользователя от VK
    def get_user(self, uid):
        params = {
            'user_ids': uid,
            'fields': 'nickname,name,sex,bdate,status',
            'access_token': token,
            'v': ver
        }
        # запрос данных VK
        response = self.get_data('users.get', params)
        user_data = response.json()
        # полученные данные в цикле переписываем в профиль
        for key in self.profile.keys():
            try:
                self.profile[key] = user_data['response'][0][key]
            except KeyError:
                pass
        # записываем ID
        self.uid = str(user_data['response'][0]['id'])
        # формируем ссылку на профиль VK
        self.link_url = VK_ID_URL + self.uid
        return user_data['response']

    # заполнение профиля данными словаря
    def set_user(self, user_data):
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
        # записываем ID
        self.uid = str(set_user_data['id'])
        # формируем ссылку на профиль VK
        self.link_url = VK_ID_URL + self.uid

    # запрос списка друзей пользователя VK
    def get_friends_list(self):
        params = {
            'user_id': self.uid,
            # 'order': 'name',
            # 'fields': 'nickname,name,sex,bdate,status',
            'access_token': token,
            'v': ver
        }
        # запрос данных VK
        response = self.get_data('friends.get', params)
        friends_data = response.json()
        self.friends = friends_data['response']
        return self.friends

    # запрос списка друзей пользователя VK
    def get_groups_list(self, extended=0):
        params = {
            'user_id': self.uid,
            'extended': '0',
            'fields': 'members_count',
            'access_token': token,
            'v': ver
        }
        # запрос данных VK
        response = self.get_data('groups.get', params)
        groups_data = response.json()
        self.groups = groups_data['response']
        return self.groups

        # запрос списка друзей пользователя VK
    def get_groups_list_extend(self):
        params = {
            'user_id': self.uid,
            'extended': '0',
            'fields': 'members_count',
            'access_token': token,
            'v': ver
        }
        # запрос данных VK
        response = self.get_data('groups.get', params)
        groups_data = response.json()
        self.groups = groups_data['response']
        return self.groups

    # запрос списка общих друзей в VK
    def get_cross_friends_list(self, src_uid, tar_uid):
        params = {
            'source_uid': src_uid,
            'target_uid': tar_uid,
            'access_token': token,
            'v': ver
            }
        # запрос данных VK
        response = self.get_data('friends.getMutual', params)
        users_data = response.json()
        return users_data['response']

    # формирование экземпляров из списка общих друзей
    def get_cross_friends(self, src_uid, tar_uid):
        cross_friends_obj = []
        cross_friends_list = self.get_cross_friends_list(src_uid, tar_uid)
        for i, friend in enumerate(cross_friends_list):
            print(i + 1,': id ',friend, sep = '')
            # создания экземпляра и запись его в список экземпляров
            cross_friends_obj.append(User({'uid': friend}))
        return cross_friends_obj

    def get_user_only_groups(self, start_group_num=0, stop_group_num=0):
        if start_group_num != 0 and stop_group_num == 0:
            stop_group_num = start_group_num

        if start_group_num == 0 and stop_group_num == 0:
            stop_group_num = self.groups['count']

        if stop_group_num < start_group_num:
            stop_group_num = self.groups['count']
        if start_group_num > stop_group_num:
            start_group_num = 0

        print(start_group_num, stop_group_num)

        offset = 0
        count = 24
        cross_groups = []
        friends_count = 0
        for num_group, group in enumerate(self.groups['items']):

            if num_group < start_group_num or num_group > stop_group_num:
                continue

            if friends_count == self.friends['count']:
                friends_count = 0
                offset = 0
            while(friends_count < self.friends['count']):
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
                                "groups =  API.groups.get({""user_id"": friends.items[friend_counter], ""extended"": 1});"
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

                response = self.get_data('execute', params)

                try:
                    exec_data= response.json()
                    #pprint(exec_data)
                    print(num_group, exec_data['response'])
                    #pprint(exec_data['response'])
                    #pprint(exec_data)
                    offset = offset + exec_data['response'][1]
                    friends_count = exec_data['response'][2]
                    if exec_data['response'][3] > 0:
                        cross_groups.append(exec_data['response'][0])
                        friends_count = self.friends['count']
                    #pprint(exec_data['response'])
                except  KeyError:
                    print('Error User')
                finally:
                    print(cross_groups)
        return cross_groups

    # выполнение запроса к VK API
    def get_data(self, method_name='', params={}, delay_time=0.0):
        time.sleep(delay_time)  # пауза чтобы VK не заблокировал соединение
        # строка запроса данных VK
        response = requests.get(M_URL + method_name, params)
        return response

if __name__ == '__main__':
    # Проверка токена
    token_true = check_token()
    if(token_true == 0):
        print('Need new token')
        exit(1)

    with WorkTimer('Group analyze'):
    # создание первого пользователя через конструктор
        User_One = User({'uid': 'eshmargunov'}) # 412548 #eshmargunov
        print(User_One.profile['first_name'], User_One.profile['last_name'])
        print(User_One)
        User_One.get_groups_list()
        pprint(User_One.groups)
        User_One.get_friends_list()
        #print('friends', User_One.friends)
        user_group_list = set()
        user_group_list = set()
        user_unique_list = set()

        for group in User_One.groups['items']:
            user_group_list.add(group)

        print('user group:', user_group_list)

        cross_groups = User_One.get_user_only_groups()
        print(cross_groups)

        cross_groups_list = set()

        for group in cross_groups:
            cross_groups_list.add(group)
        print('cross:', cross_groups_list)

        user_unique_list = user_group_list.difference(cross_groups_list)
        print('unique group:', user_unique_list)

        # with open("groups.json", "w", encoding="utf-8") as file:
        #     json.dump(User_One.groups, file)

    print(WorkTimer('Group analyze').time_work)

