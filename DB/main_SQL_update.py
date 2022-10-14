import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_SQL_update import create_tables, People, Blacklist, Favourite
from vk_application_funcs.vk_search import VK

atoken = 'vk1.a.xG33q26zjvGhC7Vx5WVnVnP0AalCHEubq8_W5JYAHONKiLOc6qJSXTPLDwyrP3laua00KiLPPjeoO2ph0GRu-0Lv2FnaqvTgWf1OAxyh4OYnhBEDFtafWsl-P-J6C3036qG5-W6H4W45xKMiLyJM5KT5b3R_xMMOJUsVAKcEDSOxJ_30lSZt3pmU-mCKdAYV'
# auser_id = 17331357
auser_id = 1583746
vk_methods = VK(atoken, auser_id)

"""
Предварительно нужно создать базу данных в командной строке операционной системы командой: 
createdb -U postgres chat_bot_vk
В переменной окружения операционной системы прописываем переменную DSN со значением 
'postgresql://postgres:1234@localhost:5432/chat_bot_vk'
где 1234 это пароль от базы данных 
"""

DSN = 'postgresql://postgres:1234@localhost:5432/chat_bot_vk'

# load_dotenv()
# DSN = os.getenv("DSN")

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def people_record_data(data: json) -> 'record SQL':
    """
    Запись данных о людях, соответствующих критериям поиска в базу данных

    :param data: данные в формате json, сгенерированные функцией vk_methods.data_maker()
    :var q_people: запрос в таблицу People базы данных для поиска существующих записей у пользователя бота
    :var id_list: лист существующих записей id vk(search_vk_id) в таблице People базы данных у пользователя бота
    :return: True, Данные записаны в таблицу People базы данных!
    :return: False, ex
    """
    try:
        q_people = session.query(People).filter(People.auser_id == auser_id)
        id_list = [record_id.search_vk_id for record_id in q_people.all()]
        for record in data:
            if record['id'] not in id_list:
                session.add(People(auser_id=auser_id, search_vk_id=record['id'], first_name=record['first_name'],
                                   last_name=record['last_name'], profile_link=record['profile_link'],
                                   photos_likes=(', '.join(record['photos']))))
                session.commit()
        return True, 'Данные записаны в таблицу People базы данных!'
    except Exception as ex:
        return False, ex


def delete_people_data(vk_id_delete: int) -> 'deleting an entry':
    """
    Удаление записи о найденных людях из базы данных

    :param vk_id_delete: существующий id vk в таблице People базы данных, который мы удаляем из базы данных
    :var q_blacklist: запрос в таблицу Blacklist БД для поиска существующих записей в черном списке у пользователя
    :var q_favourite: запрос в таблицу Favourite БД для поиска существующих записей в избранном у пользователя
    :var id_list_blacklist: существующие записи id vk(search_vk_id) в таблице Blacklist базы данных у пользователя
    :var id_list_favourite: существующие записи id vk(search_vk_id) в таблице Favourite базы данных у пользователя
    :return: True, Данные удалены из таблицы People базы данных!
    :return: False, Удалите id {vk_id_delete} из черного списка!
    :return: False, Удалите id {vk_id_delete} из избранного списка!
    :return: False, Ошибку
    """
    try:
        q_blacklist = session.query(Blacklist).filter(Blacklist.auser_id == auser_id)
        q_favourite = session.query(Favourite).filter(Favourite.auser_id == auser_id)
        id_list_blacklist = [record_id.search_vk_id for record_id in q_blacklist.all()]
        id_list_favourite = [record_id.search_vk_id for record_id in q_favourite.all()]
        if vk_id_delete not in id_list_blacklist and vk_id_delete not in id_list_favourite:
            session.query(People).filter(People.search_vk_id == vk_id_delete).delete()
            session.commit()
            return True, 'Данные удалены из таблицы People базы данных!'
        elif vk_id_delete in id_list_blacklist:
            return False, f'Удалите id {vk_id_delete} из черного списка!'
        elif vk_id_delete in id_list_favourite:
            return False, f'Удалите id {vk_id_delete} из избранного списка!'
    except Exception as ex:
        return False, ex


def blacklist_record_data(auser_id, id_blacklist: int) -> 'record blacklist SQL':
    """
    Запись данных о людях в таблицу Blacklist у пользователя бота

    :param auser_id: id пользователя бота telegram
    :param id_blacklist: id vk(search_vk_id) который пользователь бота telegram заносит в черный список
    :var q_people: запрос в таблицу People базы данных для поиска существующих записей у пользователя бота
    :var q_blacklist: запрос в таблицу Blacklist БД для поиска существующих записей в черном списке у пользователя
    :var id_list_blacklist существующие записи id vk(search_vk_id) в таблице Blacklist БД у пользователя
    :return: True, Данные записаны в таблицу Blacklist базы данных!
    :return: False, Человек уже внесен в таблицу Blacklist базы данных!
    :return: False, ex
    """
    try:
        q_people = session.query(People).filter(People.auser_id == auser_id).filter(People.search_vk_id == id_blacklist)
        q_blacklist = session.query(Blacklist).filter(Blacklist.auser_id == auser_id).filter(Blacklist.search_vk_id ==
                                                                                             id_blacklist)
        id_list_blacklist = [record_id.search_vk_id for record_id in q_blacklist.all()]
        if id_blacklist not in id_list_blacklist:
            for record in q_people.all():
                session.add(Blacklist(search_vk_id=record.search_vk_id, auser_id=auser_id, id_people=record.id))
            session.commit()
            return True, 'Данные записаны в таблицу Blacklist базы данных!'
        else:
            return False, 'Человек уже внесен в таблицу Blacklist базы данных!'
    except Exception as ex:
        return False, ex


def delete_blacklist_data(auser_id, vk_id_delete: int) -> 'deleting an entry':
    """
    Удаление записи данных о людях из таблицы Blacklist у пользователя бота

    :param auser_id: id пользователя бота telegram
    :param vk_id_delete: id vk(search_vk_id) который пользователь бота telegram удаляет из черного списка
    :return: True, Данные удалены из базы данных blacklist!
    :return: False, ex

    """
    try:
        session.query(Blacklist).filter(Blacklist.auser_id == auser_id).filter(Blacklist.search_vk_id ==
                                                                               vk_id_delete).delete()
        session.commit()
        return True, 'Данные удалены из базы данных blacklist!'
    except Exception as ex:
        return False, ex


def favourites_record_data(auser_id, id_favourite: int) -> 'record favourite SQL':
    """
    Запись данных о людях в таблицу Favourite у пользователя бота
    :param auser_id: id пользователя бота telegram
    :param id_favourite: id vk(search_vk_id) который пользователь бота telegram заносит в список избранное
    :var q_people: запрос в таблицу People базы данных для поиска существующих записей у пользователя бота
    :var q_favourite: запрос в таблицу Favourite БД для поиска существующих записей в избранном у пользователя бота
    :var id_list_favourite: существующие записи id vk(search_vk_id) в таблице Favourite базы данных у пользователя
    :return: True, Данные записаны в базу данных favourites!
    :return: False, Человек уже внесен в базу данных!
    :return: False, ex

    """
    try:
        q_people = session.query(People).filter(People.auser_id == auser_id).filter(People.search_vk_id ==
                                                                                    id_favourite)
        q_favourite = session.query(Favourite).filter(Favourite.auser_id == auser_id).filter(Favourite.search_vk_id ==
                                                                                             id_favourite)
        id_list_favourite = [record.search_vk_id for record in q_favourite.all()]
        if id_favourite not in id_list_favourite:
            for record in q_people.all():
                session.add(Favourite(auser_id=auser_id, search_vk_id=id_favourite, first_name=record.first_name,
                                      last_name=record.last_name, profile_link=record.profile_link,
                                      photos_likes=record.photos_likes, id_people=record.id))
            session.commit()
            return True, 'Данные записаны в базу данных favourites!'
        else:
            return False, 'Человек уже внесен в базу данных!'
    except Exception as ex:
        return False, ex


def delete_favourites_data(auser_id, vk_id_delete: int) -> 'deleting an entry':
    """
    Удаление записи данных о людях из таблицы Favourite у пользователя бота

    :param auser_id: id пользователя бота telegram
    :param vk_id_delete: id vk(search_vk_id) который пользователь бота telegram удаляет из списка избранного
    :return: True, Данные удалены из базы данных favourites!
    :return: False, ex

    """
    try:
        session.query(Favourite).filter(Favourite.auser_id == auser_id).filter(Favourite.search_vk_id ==
                                                                               vk_id_delete).delete()
        session.commit()
        return True, 'Данные удалены из базы данных favourites!'
    except Exception as ex:
        return False, ex


session.close()


def display_data_people(auser_id: int) -> 'id vk':
    """
    Отображение списка отобранных кандидатов с учетом проверки их отсутствия в черном списке

    :param auser_id: id пользователя бота telegram
    :var q_blacklist: запрос в таблицу Blacklist БД для поиска существующих записей в черном списке у пользователя
    :var id_list_blacklist существующие записи id vk(search_vk_id) в таблице Blacklist базы данных у пользователя
    :return: [list] data_display_people

    """
    data_display_people = []
    q_people = session.query(People).filter(People.auser_id == auser_id)
    q_blacklist = session.query(Blacklist).filter(Blacklist.auser_id == auser_id)
    id_list_blacklist = [record_id.search_vk_id for record_id in q_blacklist.all()]
    for search in q_people.all():
        if search.search_vk_id not in id_list_blacklist:
            data_display_people.append([search.id, search.auser_id, search.search_vk_id, search.first_name,
                                        search.last_name, search.profile_link, search.photos_likes])
    return data_display_people


def display_favorite(auser_id: int) -> 'id vk':
    """
    Отображение списка избранных кандидатов
    
    :param auser_id: id пользователя бота telegram
    :var q_favourite: запрос в таблицу Favourite БД для поиска существующих записей в избранном у пользователя бота
    :return: [list] data_display_favorite
    """
    data_display_favorite = []
    q_favorite = session.query(Favourite).filter(Favourite.auser_id == auser_id)
    for search in q_favorite.all():
        data_display_favorite.append([search.id, search.auser_id, search.search_vk_id, search.first_name,
                                      search.last_name, search.profile_link, search.photos_likes])
    return data_display_favorite


if __name__ == '__main__':
    display_favorite(auser_id)
