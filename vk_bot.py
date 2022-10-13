from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_search import VK, atoken, vk_methods
from main_SQL_update import people_record_data, display_data_people, favourites_record_data, blacklist_record_data

with open('token.txt') as file:
    token = file.readline()

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
peoples = vk_methods.data_maker()


# назовем базу данных vk_db

def write_msg(user_id, message, attachment=None, keyboard=None):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
        'attachment': attachment,
        'keyboard': keyboard,
    })


for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        request = event.text.lower()
        vk_user = VK(atoken, user_id)
        counter = 0
        person = peoples[counter]
        if request == 'привет':
            keyboard = VkKeyboard(one_time=True)
            buttons = ['Start', 'Пока']
            buttons_color = [VkKeyboardColor.PRIMARY, VkKeyboardColor.NEGATIVE]
            name = vk_methods.get_info()["response"][0]["first_name"]
            for button, button_color in zip(buttons, buttons_color):
                keyboard.add_button(button, button_color)
            write_msg(user_id,
                      f'Хай, {name},\nПодобрали для вас несколько вариантов,\n'
                      f'нажмите "start" чтобы начать поиск пары',
                      keyboard=keyboard)
        elif request == 'start':
            vk_user_id = person['id']
            keyboard = VkKeyboard()
            buttons = ['Like', 'Dislike', 'Add in favorite', 'Blacklist']
            buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                              VkKeyboardColor.SECONDARY]
            for button, button_color in zip(buttons, buttons_colors):
                keyboard.add_button(button, button_color)
            keyboard.add_line()
            keyboard.add_button(f'Next', VkKeyboardColor.SECONDARY)
            write_msg(user_id, f'{person["first_name"]}, {person["last_name"]}'
                               f'{person["profile_link"]}', keyboard=keyboard, attachment=','.join(person["photos"]))
        elif request == 'like':
            vk_user_id = person['id']
            # тут должна быть возможность изменить статус
        elif request == 'dislike':
            vk_user_id = person['id']
            blacklist_record_data(user_id, vk_user_id)
        elif request == 'add in favorite':
            vk_user_id = person['id']
            favourites_record_data(user_id, vk_user_id)
        elif request == 'next':
            counter += 1
            person = peoples[counter]
            vk_user_id = person['id']
            keyboard = VkKeyboard()
            buttons = ['Like', 'Dislike', 'Add in favorite', 'Blacklist']
            buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                              VkKeyboardColor.SECONDARY]
            for button, button_color in zip(buttons, buttons_colors):
                keyboard.add_button(button, button_color)
            keyboard.add_line()
            keyboard.add_button(f'Next', VkKeyboardColor.SECONDARY)
            write_msg(user_id, f'{person["first_name"]}, {person["last_name"]}'
                               f'{person["profile_link"]}', keyboard=keyboard, attachment=','.join(person["photos"]))

        elif request == 'пока':
            write_msg(user_id, 'Пока((')
        else:
            write_msg(user_id, 'Не поняла вашего ответа...')
