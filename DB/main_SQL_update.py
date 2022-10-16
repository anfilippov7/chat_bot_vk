import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from DB.models_SQL_update import create_tables, People, Blacklist, Favourite
from vk_search import VK, vk_application_token, my_id

vk_methods = VK(vk_application_token, my_id)

"""
Предварительно нужно создать БД в командной строке операционной системы командой: createdb -U postgres chat_bot_vk
"""

DSN = 'postgresql://postgres:1234@localhost:5432/chat_bot_vk'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()


def people_record_data(data: json) -> 'record SQL':
    """ Запись данных о людях, соответствующих критериям поиска в базу данных у пользователя бота

    :param data: данные в формате json, сгенерированные функцией vk_methods.data_maker()
    :var q_people: запрос в таблицу People базы данных для поиска существующих записей
    :var id_list: лист существующих записей id vk(search_vk_id) в таблице People базы данных
    :return: True, Данные записаны в таблицу People базы данных!
    :return: False, ex

    """
    try:
        q_people = session.query(People).filter(People.my_id == my_id)
        id_list = [record_id.search_vk_id for record_id in q_people.all()]
        for record in data:
            if record['id'] not in id_list:
                session.add(People(my_id=my_id, search_vk_id=record['id'], first_name=record['first_name'],
                                   last_name=record['last_name'], profile_link=record['profile_link'],
                                   photos_likes=(','.join(record['photos']))))
                session.commit()
        return True, 'Данные записаны в таблицу People базы данных!'
    except Exception as ex:
        return False, ex


def delete_people_data(vk_id_delete: int) -> 'deleting an entry':
    """ Удаление записи о найденных людях из базы данных

    :param vk_id_delete: существующий id vk в таблице People базы данных, который мы удаляем из базы данных
    :var q_blacklist: запрос в таблицу Blacklist базы данных для поиска существующих записей в черном списке
    :var q_favourite: запрос в таблицу Favourite базы данных для поиска существующих записей в избранном
    :var id_list_blacklist: лист существующих записей id vk(search_vk_id) в таблице Blacklist базы данных
    :var id_list_favourite: лист существующих записей id vk(search_vk_id) в таблице Favourite базы данных
    :return: True, Данные удалены из таблицы People базы данных!
    :return: False, Удалите id {vk_id_delete} из черного списка!
    :return: False, Удалите id {vk_id_delete} из избранного списка!
    :return: False, ex

    """
    try:
        q_blacklist = session.query(Blacklist).filter(Blacklist.my_id == my_id)
        q_favourite = session.query(Favourite).filter(Favourite.my_id == my_id)
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


def blacklist_record_data(my_id, id_blacklist: int) -> 'record blacklist SQL':
    """ Запись данных о людях в таблицу Blacklist у пользователя бота

    :param auser_id: id пользователя бота telegram
    :param id_blacklist: id vk(search_vk_id) который пользователь бота telegram заносит в черный список
    :var q_people: запрос в таблицу People базы данных для поиска существующих записей у пользователя бота
    :var q_blacklist: запрос в таблицу Blacklist базы данных для поиска существующих записей в черном списке
    :var id_list_blacklist лист существующих записей id vk(search_vk_id) в таблице Blacklist базы данных
    :return: True, Данные записаны в таблицу Blacklist базы данных!
    :return: False, Человек уже внесен в таблицу Blacklist базы данных!
    :return: False, ex

    """
    try:
        q_people = session.query(People).filter(People.auser_id == my_id).filter(People.search_vk_id == id_blacklist)
        q_blacklist = session.query(Blacklist).filter(Blacklist.auser_id == my_id).filter(Blacklist.search_vk_id ==
                                                                                          id_blacklist)
        id_list_blacklist = [record_id.search_vk_id for record_id in q_blacklist.all()]
        if id_blacklist not in id_list_blacklist:
            for record in q_people.all():
                session.add(Blacklist(search_vk_id=record.search_vk_id, my_id=my_id, id_people=record.id))
            session.commit()
            return True, 'Данные записаны в таблицу Blacklist базы данных!'
        else:
            return False, 'Человек уже внесен в таблицу Blacklist базы данных!'
    except Exception as ex:
        return False, ex


def delete_blacklist_data(my_id, vk_id_delete: int) -> 'deleting an entry':
    """ Удаление записи данных о людях из таблицы Blacklist у пользователя бота

    :param auser_id: id пользователя бота telegram
    :param vk_id_delete: id vk(search_vk_id) который пользователь бота telegram удаляет из черного списка
    :return: True, Данные удалены из базы данных blacklist!
    :return: False, ex

    """
    try:
        session.query(Blacklist).filter(Blacklist.my_id == my_id).filter(Blacklist.search_vk_id ==
                                                                         vk_id_delete).delete()
        session.commit()
        return True, 'Данные удалены из базы данных blacklist!'
    except Exception as ex:
        return False, ex


def favourites_record_data(my_id, id_favourite: int) -> 'record favourite SQL':
    """ Запись данных о людях в таблицу Favourite у пользователя бота

    :param auser_id: id пользователя бота telegram
    :param id_favourite: id vk(search_vk_id) который пользователь бота telegram заносит в список избранное
    :var q_people: запрос в таблицу People базы данных для поиска существующих записей
    :var q_favourite: запрос в таблицу Favourite базы данных для поиска существующих записей в избранном
    :var id_list_favourite: лист существующих записей id vk(search_vk_id) в таблице Favourite базы данных
    :return: True, Данные записаны в базу данных favourites!
    :return: False, Человек уже внесен в базу данных!
    :return: False, ex

    """
    try:
        q_people = session.query(People).filter(People.my_id == my_id).filter(People.search_vk_id == id_favourite)
        q_favourite = session.query(Favourite).filter(Favourite.my_id == my_id).filter(Favourite.search_vk_id ==
                                                                                       id_favourite)
        id_list_favourite = [record.search_vk_id for record in q_favourite.all()]
        if id_favourite not in id_list_favourite:
            for record in q_people.all():
                session.add(Favourite(my_id=my_id, search_vk_id=id_favourite, first_name=record.first_name,
                                      last_name=record.last_name, profile_link=record.profile_link,
                                      photos_likes=record.photos_likes, id_people=record.id))
            session.commit()
            return True, 'Данные записаны в базу данных favourites!'
        else:
            return False, 'Человек уже внесен в базу данных!'
    except Exception as ex:
        return False, ex


def delete_favourites_data(my_id, vk_id_delete: int) -> 'deleting an entry':
    """ Удаление записи данных о людях из таблицы Favourite у пользователя бота

    :param auser_id: id пользователя бота telegram
    :param vk_id_delete: id vk(search_vk_id) который пользователь бота telegram удаляет из списка избранного
    :return: True, Данные удалены из базы данных favourites!
    :return: False, ex

    """
    try:
        session.query(Favourite).filter(Favourite.my_id == my_id).filter(
            Favourite.search_vk_id == vk_id_delete).delete()
        session.commit()
        return True, 'Данные удалены из базы данных favourites!'
    except Exception as ex:
        return False, ex


session.close()


def display_data_people(my_id: int) -> 'id vk':
    """ Отображение списка отобранных кандидатов с учетом проверки их отсутствия в черном списке

    :param auser_id: id пользователя бота telegram
    :var q_blacklist: запрос в таблицу Blacklist базы данных для поиска существующих записей в черном списке
    :var id_list_blacklist лист существующих записей id vk(search_vk_id) в таблице Blacklist базы данных
    :return: [list] data_display_people

    """
    data_display_people = []
    q_people = session.query(People).filter(People.my_id == my_id)
    q_blacklist = session.query(Blacklist).filter(Blacklist.my_id == my_id)
    id_list_blacklist = [record_id.search_vk_id for record_id in q_blacklist.all()]
    for search in q_people.all():
        if search.search_vk_id not in id_list_blacklist:
            data_display_people.append([search.id, search.my_id, search.search_vk_id, search.first_name,
                                        search.last_name, search.profile_link, search.photos_likes])
    return data_display_people


def display_favorite(my_id: int) -> 'id vk':
    """ Отображение списка избранных кандидатов

    :param auser_id: id пользователя бота telegram
    :var q_favourite: запрос в таблицу Favourite базы данных для поиска существующих записей в избранном
    :return: [list] data_display_favorite

    """
    data_display_favorite = []
    q_favorite = session.query(Favourite).filter(Favourite.my_id == my_id)
    for search in q_favorite.all():
        data_display_favorite.append([search.id, search.my_id, search.search_vk_id, search.first_name,
                                      search.last_name, search.profile_link, search.photos_likes])
    return data_display_favorite


# if __name__ == '__main__':
#     people_record_data(vk_methods.data_maker())
    # delete_people_data(602676)
    # blacklist_record_data(my_id, 50183)
    # delete_blacklist_data(my_id, 50183)
    # favourites_record_data(my_id, 133737442)
    # delete_favourites_data(my_id, 602676)
    # print(display_data_people(my_id))
    # display_favorite(my_id)
