import requests
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
token = 'c2798ba0462903dff1c1f1a3ca833f5fb058f7af8e30a87e75f33d311e4362bc16ebfa83b7f41fe91666c'
ver = '5.52'  # версия API

# функция проверки актуальности токена
def check_token():
    response = requests.get(M_URL + 'users.get', {'user_ids': '1', 'access_token': token, 'v': ver})
    conn_state = response.json()
    for state, val_state in conn_state.items():
        if state == 'error':
            if(val_state['error_code']) == 5:
                return 0
    return 1

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
    # инициализация обьекта
    def __init__(self, settings={'obj_name': '', 'uid': '','profile_data': ''}):
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
        self.link_url = VK_ID_URL +  self.uid
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
            'order': 'name',
            'fields': 'nickname,name,sex,bdate,status',
            'access_token': token,
            'v': ver
        }
        # запрос данных VK
        response = self.get_data('friends.get', params)
        users_data = response.json()
        return users_data

    # запрос списка общиз друзей в VK
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
        return users_data

    # формирование экземпляров из списка общих друзей
    def get_cross_friends(self, src_uid, tar_uid):
        cross_friends_obj = []
        cross_friends_list = self.get_cross_friends_list(src_uid, tar_uid)
        for i, friend in enumerate(cross_friends_list['response']):
            print(i + 1,': id ',friend, sep = '')
            # создания экземпляра и запись его в список экземпляров
            cross_friends_obj.append(User({'uid': friend}))
        return cross_friends_obj

    # выполнение запроса к VK API
    def get_data(self, method_name='', params={}):
        # пауза чтобы VK не заблокировал соединение
        time.sleep(0.3)
        # строка запроса данных VK
        response = requests.get(M_URL + method_name, params)
        return response

if __name__ == '__main__':
    # Проверка токена
    token_true = check_token()
    if(token_true == 0):
        print('Need new token')
        exit(1)

    # создание первого пользователя через конструктор
    User_One = User({'uid': '9317'})
    print(User_One.profile['first_name'], User_One.profile['last_name'])
    print(User_One)

    # создание второго пользователя через метод get_user
    User_Two = User()
    User_Two.get_user('736242')
    print(User_Two.profile['first_name'], User_Two.profile['last_name'])
    print(User_Two)

    print('Поиск общих друзей...')
    # поиск общих друзй пользователей с применением оператора &
    cross_friends = User_Two & User_One

    # вывод списка общих друзей
    print('\nОбщие друзья:')
    for friend in cross_friends:
        print(friend.profile['first_name'], friend.profile['last_name'])
        print(friend)
