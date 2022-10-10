import requests
from pprint import pprint
import time


class VK:

    def __init__(self, token: str, user_id: int):
        self.token = token
        self.user_id = user_id
        self.params = {'v': '5.131', 'access_token': self.token}
        self.data_list = []

    def get_info(self) -> dict:
        url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': self.user_id,
            'fields': 'sex, city, bdate'
        }
        response = requests.get(url, params={**params, **self.params})
        return response.json()

    def search_people(self) -> dict:
        url = 'https://api.vk.com/method/users.search'
        info_dict = self.get_info()
        try:
            birthday_year = info_dict['response'][0]['bdate'].split('.')[2]
        except KeyError:
            birthday_year = 2000
        try:
            sex = info_dict['response'][0]['sex']
        except KeyError:
            sex = 0
        try:
            city = info_dict['response'][0]['city']['id']
        except KeyError:
            city = None

        if sex == 1:
            params = {
                'count': 100,
                'sex': 2,
                'birth_year': int(birthday_year),
                'has_photo': 1,
                'city': city,
                'status': 1 or 6,
                'sort': 0,
                'fields': 'is_closed',
            }
        else:
            params = {
                'count': 100,
                'sex': 1,
                'birth_year': int(birthday_year),
                'has_photo': 1,
                'city': city,
                'status': 1 or 6,
                'sort': 0,
                'fields': 'is_closed',
            }
        response = requests.get(url, params={**params, **self.params})
        return response.json()

    def get_photo(self, user_id) -> list:
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'rev': 0,
        }
        response = requests.get(url, params={**params, **self.params})
        info = []
        some_list = sorted(response.json()['response']['items'], key=lambda x: -x['likes']['count'])
        for i in some_list:
            info.append(f'photo{i["owner_id"]}_{i["id"]}')
            if len(info) == 3:
                break
            else:
                continue
        return info

    def data_maker(self):
        for item in self.search_people()['response']['items']:
            if not item['is_closed']:
                data = {}
                data.setdefault('first_name', item['first_name'])
                data.setdefault('last_name', item['last_name'])
                data.setdefault('id', item['id'])
                data.setdefault('profile_link', f'https://vk.com/id{item["id"]}')
                data.setdefault('photos', self.get_photo(item['id']))
                self.data_list.append(data)
                time.sleep(0.3)
            else:
                continue
        return self.data_list


atoken = 'vk1.a.xG33q26zjvGhC7Vx5WVnVnP0AalCHEubq8_W5JYAHONKiLOc6qJSXTPLDwyrP3laua00KiLPPjeoO2ph0GRu-0Lv2FnaqvTgWf1OAxyh4OYnhBEDFtafWsl-P-J6C3036qG5-W6H4W45xKMiLyJM5KT5b3R_xMMOJUsVAKcEDSOxJ_30lSZt3pmU-mCKdAYV'
auser_id = 1583746
vk_methods = VK(atoken, auser_id)
pprint(vk_methods.data_maker())
