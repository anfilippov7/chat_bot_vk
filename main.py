
import requests
from pprint import pprint
from VK import VK
from datetime import datetime
# import json

def age ():   ## Метод вычисляет возраст
    info = vk.users_info()
    date_now = datetime.today()
    day_now = date_now.day
    month_now = date_now.month
    year_now = date_now.year
    user_bdate = info['response'][0]['bdate']
    day_user = int(user_bdate.split('.')[0])
    month_user = int(user_bdate.split('.')[1])
    year_user = int(user_bdate.split('.')[2])

    user_age = year_now - year_user
    if month_now < month_user:
        user_age -= 1
    elif month_now == month_user and day_now < day_user:
        user_age -= 1
    return user_age

if __name__ == '__main__':

#Считываем токен для доступа в API_vk из файла 'token_vk.txt'
    with open('token_vk.txt', "r") as file_object:
        token_vk = file_object.read().strip()
#Считываем ID пользователя vk из файла 'ID_vk.txt'
    with open('ID_vk.txt', "r") as file_object:
        ID_vk = file_object.read().strip()

    vk = VK(token_vk, ID_vk)
    qty_photos = vk.users_photos()['response']['count']
    print(f"У пользователя {qty_photos} фотографий")
    print(f'Возраст пользователя {age()} лет')
    pprint(vk.users_info())

    dict_photos = vk.users_photos()['response']['items']
    print("Информация о фотографиях получена")
    pprint(vk.get_list_photos(dict_photos=dict_photos, qty_photos=qty_photos))

