# chat_bot_vk
# Для корректной работы программы необходимо зайти в папку VK в основном каталоге и поместить в файл "tokens.py" токена:
 - ```vk_bot_token``` (подробная инструкция по получению вк токена по ссылке https://faq.botmechanic.io/vk-token)
 - ```vk_application_token``` (подробная инструкция по получению vk app token по ссылке https://dvmn.org/encyclopedia/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/)
 - ```my_id``` - цифровое значение идентификатора пользователя (вам VK ID)
 ***
 # __Описание работы VK бота__
 Пользователь вступает в сообщество VK и начинает диалог с сообществом.
 Первое сообщение для начала взаимодействия с ботом слово 'привет'.
 После чего бот выведет две кнопки "Start" и "пока".
 Кнопка "Start" запустит алгоритм поиска пары по следующим ключевым пунктам:
 - Город в котором вы проживаете
 - Семейное положение пользователя
 - Доступ к странице

 Также у вас появятся слдеющие кнопки:
  - ```"next"``` - выдаст вам следующую кандидатуру
  - ```"add to blacklist"``` - добавит текущего кандидата в черный список
  - ```"add to favorite"``` - добавит текущего кандидата в список избранных
  - ```"favorites"``` - выведет всех людей, которые находятся в списке избранных
  - ```"пока"``` - закончит сеанс с ботом
