import requests
from pprint import pprint
import time


class VK:

    def __init__(self, token: str, user_id: int):
        self.token = token
        self.user_id = user_id
        self.params = {'v': '5.131', 'access_token': self.token}

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
        birsday_year = info_dict['response'][0]['bdate'].split('.')[2]
        sex = info_dict['response'][0]['sex']
        city = info_dict['response'][0]['city']['id']
        if sex == 1:
            params = {
                'count': 10,
                'sex': 2,
                'birth_year': int(birsday_year),
                'has_photo': 1,
                'city': city
            }
        else:
            params = {
                'count': 10,
                'sex': 1,
                'birth_year': int(birsday_year),
                'has_photo': 1,
                'city': city
            }
        response = requests.get(url, params={**params, **self.params})
        return response.json()

    def get_photo(self) -> list:
        second_data_list = []
        url = 'https://api.vk.com/method/photos.get'
        for item in self.search_people()['response']['items']:
            info = {}
            params = {
                'owner_id': item['id'],
                'album_id': 'profile',
                'extended': 1
            }
            response = requests.get(url, params={**params, **self.params})
            if 'error' not in response.json().keys():
                time.sleep(1)
                some_list = sorted(response.json()['response']['items'], key=lambda x: -x['likes']['count'])
                info.setdefault('owner_id', some_list[0]['owner_id'])
                info.setdefault('first_likes', f'photo{some_list[0]["owner_id"]}_{some_list[0]["id"]}')
                info.setdefault('second_likes', f'photo{some_list[1]["owner_id"]}_{some_list[1]["id"]}')
                info.setdefault('third_likes', f'photo{some_list[2]["owner_id"]}_{some_list[2]["id"]}')
                second_data_list.append(info)
            else:
                continue
        return second_data_list

    def data_maker(self):
        list_data = []
        for item in self.search_people()['response']['items']:
            data = {}
            data.setdefault('first_name', item['first_name'])
            data.setdefault('last_name', item['last_name'])
            data.setdefault('id', item['id'])
            data.setdefault('profile_link', f'https://vk.com/id{item["id"]}')
            for point in self.get_photo():
                if point['owner_id'] == item['id']:
                    data.setdefault('first_likes', point['first_likes'])
                    data.setdefault('second_likes', point['second_likes'])
                    data.setdefault('third_likes', point['third_likes'])
            list_data.append(data)
        return list_data


atoken = 'vk1.a.xG33q26zjvGhC7Vx5WVnVnP0AalCHEubq8_W5JYAHONKiLOc6qJSXTPLDwyrP3laua00KiLPPjeoO2ph0GRu-0Lv2FnaqvTgWf1OAxyh4OYnhBEDFtafWsl-P-J6C3036qG5-W6H4W45xKMiLyJM5KT5b3R_xMMOJUsVAKcEDSOxJ_30lSZt3pmU-mCKdAYV'
auser_id = 1583746
vk_methods = VK(atoken, auser_id)
pprint(vk_methods.data_maker())


