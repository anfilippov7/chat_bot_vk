from vk_api.longpoll import VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from DB.main_SQL_update import favourites_record_data, blacklist_record_data, display_favorite
from vk_application_funcs.bot_funcs import vk_user, write_msg, longpoll, peoples


def main():
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            counter = 0
            person = peoples[counter]
            if request == 'привет':
                my_keyboard = VkKeyboard(one_time=True)
                buttons = ['Start', 'Пока']
                buttons_color = [VkKeyboardColor.PRIMARY, VkKeyboardColor.NEGATIVE]
                name = vk_user.get_info()["response"][0]["first_name"]
                for i, j in zip(buttons, buttons_color):
                    my_keyboard.add_button(i, j)
                write_msg(user_id=event.user_id,
                          message=f'Хай, {name},\nПодобрали для вас несколько вариантов,\n'
                                  f'нажмите "start" чтобы начать поиск пары',
                          keyboard=my_keyboard)
            elif request == 'start':
                my_keyboard = VkKeyboard()
                buttons = ['Blacklist', 'Favorites', 'Add to favorite', 'Add to Blacklist']
                buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                                  VkKeyboardColor.SECONDARY]
                for button, button_color in zip(buttons, buttons_colors):
                    my_keyboard.add_button(button, button_color)
                my_keyboard.add_line()
                my_keyboard.add_button(f'Next', VkKeyboardColor.SECONDARY)
                write_msg(event.user_id, f'{person["first_name"]}, {person["last_name"]}\n'
                                         f'{person["profile_link"]}', keyboard=my_keyboard,
                          attachment=','.join(person["photos"]))
            elif request == 'add to blacklist':
                vk_user_id = person['id']
                blacklist_record_data(event.user_id, vk_user_id)
            elif request == 'add to favorite':
                vk_user_id = person['id']
                favourites_record_data(event.user_id, vk_user_id)
            elif request == 'favorites':
                display_favorite(event.user_id)
                write_msg(event.user_id, display_favorite(event.user_id))
            elif request == 'next':
                counter += 1
                person = peoples[counter]
                my_keyboard = VkKeyboard()
                buttons = ['Blacklist', 'Favorites', 'Add to favorite', 'Add to Blacklist']
                buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                                  VkKeyboardColor.SECONDARY]
                for button, button_color in zip(buttons, buttons_colors):
                    my_keyboard.add_button(button, button_color)
                my_keyboard.add_line()
                my_keyboard.add_button(f'Next', VkKeyboardColor.SECONDARY)
                write_msg(event.user_id, f'{person["first_name"]}, {person["last_name"]}'
                                         f'{person["profile_link"]}', keyboard=my_keyboard,
                          attachment=','.join(person["photos"]))
            elif request == 'blacklist':
                write_msg(event.user_id, 'зачем портить себе настроение')
            elif request == 'пока':
                write_msg(event.user_id, 'Пока((')
            else:
                write_msg(event.user_id, 'Не поняла вашего ответа...')


if __name__ == '__main__':
    main()
