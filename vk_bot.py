from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_search import VK, atoken, vk_methods

with open('token.txt') as file:
    token = file.readline()

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
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
        if request == 'привет':
            keyboard = VkKeyboard(one_time=True)
            buttons = ['Start', 'Пока']
            buttons_color = [VkKeyboardColor.PRIMARY, VkKeyboardColor.NEGATIVE]
            write_msg(user_id, f'Хай, {user_id}', keyboard=keyboard)
            ## здесь создаем таблицу в бд, где user_id = имя таблицы!
        elif request == 'start':
            for user in vk_methods.search_people(): # здесь должна быть база данных
                # здесь проверка есть ли юзер в таблицах
                keyboard = VkKeyboard()
                buttons = ['Like', 'Dislike', 'Add in favorite', 'Blacklist']
                buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                                  VkKeyboardColor.SECONDARY]
                for button, button_color in zip(buttons, buttons_colors):
                    keyboard.add_button(button, button_color)
                write_msg(user_id,
                          f'{user["first_name"]} {user["second_name"]}'
                          f'{user["profile_link"]}',
                          attachment=f'{user["first_likes"]},{user["second_likes"]},{user["third_likes"]}',
                          keyboard=keyboard)
                break
        elif request == 'like':

        elif request == 'пока':
            write_msg(user_id, 'Пока((')
        else:
            write_msg(user_id, 'Не поняла вашего ответа...')
