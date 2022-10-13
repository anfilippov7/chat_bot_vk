from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll
from vk_application_funcs.vk_search import VK, vk_application_token, vk_bot_token, my_id

vk = vk_api.VkApi(token=vk_bot_token)
longpoll = VkLongPoll(vk)
vk_user = VK(vk_application_token, my_id)
peoples = vk_user.data_maker()


def write_msg(user_id, message, attachment=None, keyboard=None):
    """
    Функция для отправки сообщени пользователю через метод VK API
    :param user_id: int: идентификатор пользователя, которому будет отправлено сообщение
    :param message: str: текст сообщения, которое будет отправлено
    :param attachment: str: необязательный параметр, если в сообщении будут прикрепленные файлы
    :param keyboard: str: необязательный параметр, с помощью VK API создает кнопки для удобного взаимодействия с ботом
    :return: None
    """
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
        'attachment': attachment,
        'keyboard': keyboard.get_keyboard(),
    })
