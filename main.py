from vk_api.longpoll import VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from DB.main_SQL_update import favourites_record_data, blacklist_record_data, display_favorite, display_data_people, \
    people_record_data
from VK.bot_funcs import vk_user, write_msg, longpoll
from vk_search import VK, vk_application_token, my_id

vk_methods = VK(vk_application_token, my_id)


def main():
    counter_people = 0
    people_record_data(vk_methods.data_maker())
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            person = display_data_people(event.user_id)
            favourite = display_favorite(event.user_id)
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
                buttons = ['Favorites', 'Add to favorite', 'Add to Blacklist']
                buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                                  VkKeyboardColor.SECONDARY]
                for button, button_color in zip(buttons, buttons_colors):
                    my_keyboard.add_button(button, button_color)
                my_keyboard.add_line()
                my_keyboard.add_button(f'Next', VkKeyboardColor.SECONDARY)
                write_msg(event.user_id, f'{person[0][3]}, {person[0][4]}, {person[0][5]}', keyboard=my_keyboard,
                          attachment=person[0][6])
            elif request == 'next':
                if counter_people < len(person) - 1:
                    counter_people += 1
                else:
                    counter_people = 0
                my_keyboard = VkKeyboard()
                buttons = ['Favorites', 'Add to favorite', 'Add to Blacklist']
                buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                                  VkKeyboardColor.SECONDARY]
                for button, button_color in zip(buttons, buttons_colors):
                    my_keyboard.add_button(button, button_color)
                my_keyboard.add_line()
                my_keyboard.add_button(f'Next', VkKeyboardColor.SECONDARY)
                write_msg(event.user_id, f'{person[counter_people][3]}, {person[counter_people][4]},'
                                         f'{person[counter_people][5]}', keyboard=my_keyboard,
                          attachment=person[counter_people][6])
            elif request == 'add to blacklist':
                vk_user_id = person[counter_people][2]
                blacklist_record_data(event.user_id, vk_user_id)
            elif request == 'add to favorite':
                vk_user_id = person[counter_people][2]
                favourites_record_data(event.user_id, vk_user_id)
            elif request == 'favorites':
                my_keyboard = VkKeyboard()
                buttons = ['Favorites', 'Add to favorite', 'Add to Blacklist']
                buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                                  VkKeyboardColor.SECONDARY]
                for button, button_color in zip(buttons, buttons_colors):
                    my_keyboard.add_button(button, button_color)
                my_keyboard.add_line()
                my_keyboard.add_button(f'Next', VkKeyboardColor.SECONDARY)
                write_msg(event.user_id, f'Список Favorites:', keyboard=my_keyboard)
                for count in range(len(favourite)):
                    write_msg(event.user_id, f'{favourite[count][3]}, {favourite[count][4]}, {favourite[count][5]}',
                              keyboard=my_keyboard)
            elif request == 'пока':
                my_keyboard = VkKeyboard()
                buttons = ['Favorites', 'Add to favorite', 'Add to Blacklist']
                buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                                  VkKeyboardColor.SECONDARY]
                for button, button_color in zip(buttons, buttons_colors):
                    my_keyboard.add_button(button, button_color)
                my_keyboard.add_line()
                my_keyboard.add_button(f'Next', VkKeyboardColor.SECONDARY)
                write_msg(event.user_id, 'Пока', keyboard=my_keyboard)
            else:
                my_keyboard = VkKeyboard()
                buttons = ['Favorites', 'Add to favorite', 'Add to Blacklist']
                buttons_colors = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY,
                                  VkKeyboardColor.SECONDARY]
                for button, button_color in zip(buttons, buttons_colors):
                    my_keyboard.add_button(button, button_color)
                my_keyboard.add_line()
                my_keyboard.add_button(f'Next', VkKeyboardColor.SECONDARY)
                write_msg(event.user_id, 'Пока', keyboard=my_keyboard)


if __name__ == '__main__':
    main()


