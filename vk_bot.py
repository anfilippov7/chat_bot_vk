from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_search import VK, atoken

with open('token.txt') as file:
    token = file.readline()

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})


for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        request = event.text.lower()
        vk_user = VK(atoken, user_id)
        if request == 'привет':
            write_msg(user_id, f'Хай, {user_id}')
        elif request == '/start':
            write_msg(user_id, f'мы нашли для вас кандидатов')
        elif request == '/next':
            for item in vk_user.data_maker():
                write_msg(user_id, f'{item["first_name"]}{item["last_name"]}\n'
                                   f'{item["profile_link"]}')
        elif request == 'пока':
            write_msg(user_id, 'Пока((')
        else:
            write_msg(user_id, 'Не поняла вашего ответа...')
