import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models_SQL_update import create_tables, People, Blacklist, Favourite
from vk_search import VK

atoken = 'vk1.a.xG33q26zjvGhC7Vx5WVnVnP0AalCHEubq8_W5JYAHONKiLOc6qJSXTPLDwyrP3laua00KiLPPjeoO2ph0GRu-0Lv2FnaqvTgWf1OAxyh4OYnhBEDFtafWsl-P-J6C3036qG5-W6H4W45xKMiLyJM5KT5b3R_xMMOJUsVAKcEDSOxJ_30lSZt3pmU-mCKdAYV'
# auser_id = 17331357

auser_id = 1583746
vk_methods = VK(atoken, auser_id)

# Предварительно нужно создать базу данных в командной строке операционной системы командой: createdb -U postgres chat_bot_vk

DSN = 'postgresql://postgres:1234@localhost:5432/chat_bot_vk'

# В переменной окружения операционной системы прописываем переменную DSN со значением 'postgresql://postgres:1234@localhost:5432/chat_bot_vk'
# где 1234 это пароль от базы данных (у каждого разработчика может отличаться)

# load_dotenv()
# DSN = os.getenv("DSN")

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def people_record_data(data: json) -> 'record SQL':
    # Записываем данные в таблицу People базы данных
    try:
        q_people = session.query(People).filter(People.auser_id == auser_id) #Делаем запрос в базу данных People у конкретного auser_id
        id_list = [record_id.search_vk_id for record_id in q_people.all()] #Делаем list comprehensions с существующими id в базе данных People у конкретного auser_id
        for record in data:
            if record['id'] not in id_list: #Если id в выборке функции vk_methods.data_maker() отсутствует в базе данных (в list comprehensions), делаем запись в БД
                session.add(People(auser_id=auser_id, search_vk_id=record['id'], first_name=record['first_name'], last_name=record['last_name'],
                            profile_link=record['profile_link'], first_likes=record['first_likes'],
                            second_likes=record['second_likes'], third_likes=record['third_likes']))
                session.commit()
        print(f'Данные записаны в базу данных people!')
        return True
    except Exception as ex:
        print(f'Все данные уже были загружены в базу данных!', ex)
        return False, ex


def delete_people_data(search_vk_id_delete: int) -> 'deleting an entry':
    # Удаляем запись из базы данных People
    try:
        q_blacklist = session.query(Blacklist).filter(Blacklist.auser_id == auser_id) #Делаем запрос в базу данных Blacklist
        q_favourite = session.query(Favourite).filter(Favourite.auser_id == auser_id) #Делаем запрос в базу данных Favourite
        id_list_blacklist = [record_id.search_vk_id for record_id in q_blacklist.all()] #Делаем list comprehensions с существующими id в базе данных Blacklist
        id_list_favourite = [record_id.search_vk_id for record_id in q_favourite.all()] #Делаем list comprehensions с существующими id в базе данных Favourite
        if search_vk_id_delete not in id_list_blacklist and search_vk_id_delete not in id_list_favourite:
            session.query(People).filter(People.search_vk_id == search_vk_id_delete).delete()
            session.commit()
            # print(f'Данные удалены из базы данных people!')
        elif search_vk_id_delete in id_list_blacklist:
            print(f'Удалите id {search_vk_id_delete} из черного списка!')
        elif search_vk_id_delete in id_list_favourite:
            print(f'Удалите id {search_vk_id_delete} из избранного списка!')
        return True
    except Exception as ex:
        # print(f'Данной записи нет в базе данных people!', ex)
        return False, ex


def blacklist_record_data(auser_id, id_blacklist: int) -> 'record blacklist SQL':
    # Записываем данные в таблицу Blacklist базы данных
    try:
        q_people = session.query(People).filter(People.auser_id == auser_id).filter(People.search_vk_id == id_blacklist)
        q_blacklist = session.query(Blacklist).filter(Blacklist.auser_id == auser_id).filter(Blacklist.search_vk_id == id_blacklist) #Делаем запрос в базу данных Blacklist
        id_list_blacklist = [record_id.search_vk_id for record_id in q_blacklist.all()] #Делаем list comprehensions с существующими id в базе данных Blacklist
        if id_blacklist not in id_list_blacklist:
            for record in q_people.all():
                session.add(Blacklist(search_vk_id=record.search_vk_id, auser_id=auser_id, id_people=record.id))
            session.commit()
            print(f'Данные записаны в базу данных blacklist!')
        else:
            print('Человек уже внесен в базу данных!')
        return True
    except Exception as ex:
        # print(f'Все или часть данных уже были загружены в базу данных blacklist!', ex)
        return False, ex

def delete_blacklist_data(auser_id, search_vk_id_delete: int) -> 'deleting an entry':
    # Удаляем запись из базы данных Blacklist
    try:
        session.query(Blacklist).filter(Blacklist.auser_id == auser_id).filter(Blacklist.search_vk_id == search_vk_id_delete).delete()
        session.commit()
        print(f'Данные удалены из базы данных blacklist!')
        return True
    except Exception as ex:
        print(f'Данной записи нет в базе данных blacklist!', ex)
        return False, ex


def favourites_record_data(auser_id, id_favourite: int) -> 'record favourite SQL':
    # Записываем данные в таблицу Favourite базы данных
    try:
        q_people = session.query(People).filter(People.auser_id == auser_id).filter(People.search_vk_id == id_favourite)
        q_favourite = session.query(Favourite).filter(Favourite.auser_id == auser_id).filter(Favourite.search_vk_id == id_favourite) #Делаем запрос в базу данных Favourite
        id_list_favourite = [record.search_vk_id for record in q_favourite.all()] #Делаем list comprehensions с существующими id в базе данных Favourite
        if id_favourite not in id_list_favourite:
            for record in q_people.all():
                session.add(Favourite(auser_id=auser_id, search_vk_id=id_favourite, first_name=record.first_name, last_name=record.last_name,
                            profile_link=record.profile_link, first_likes=record.first_likes,
                            second_likes=record.second_likes, third_likes=record.third_likes, id_people=record.id))
            session.commit()
            print(f'Данные записаны в базу данных favourites!')
            return True
        else:
            print('Человек уже внесен в базу данных!')
            return True
    except Exception as ex:
        # print(f'Все или часть данных уже были загружены в базу данных favourites!', ex)
        return False, ex


def delete_favourites_data(auser_id, search_vk_id_delete: int) -> 'deleting an entry':
    # Удаляем запись из базы данных Favourite
    try:
        session.query(Favourite).filter(Favourite.auser_id == auser_id).filter(Favourite.search_vk_id == search_vk_id_delete).delete()
        session.commit()
        print(f'Данные удалены из базы данных favourites!')
        return True
    except Exception as ex:
        print(f'Данной записи нет в базе данных favourites!', ex)
        return False, ex


session.close()


def join_people_favourites(auser_id, id_favourite: int):
    #Джойним таблицы people и favourite
    query = session.query(People, Favourite).filter(People.auser_id == auser_id).filter(People.search_vk_id == id_favourite)
    query = query.join(Favourite, Favourite.search_vk_id == People.search_vk_id)
    records = query.all()
    for people, favourite in records:
        # print(people.search_vk_id, favourite.search_vk_id)
        return people.search_vk_id, favourite.search_vk_id


def join_people_blacklist(auser_id, id_blacklist: int):
    #Джойним таблицы people и blacklist
    query = session.query(People, Blacklist).filter(People.auser_id == auser_id).filter(People.search_vk_id == id_blacklist)
    query = query.join(Blacklist, Blacklist.search_vk_id == People.search_vk_id)
    records = query.all()
    for people, blacklist in records:
        return people.search_vk_id, blacklist.search_vk_id


def display_data_people(auser_id: int):
    q_people = session.query(People).filter(People.auser_id == auser_id)
    q_blacklist = session.query(Blacklist).filter(Blacklist.auser_id == auser_id) # Делаем запрос в базу данных Blacklist
    id_list_blacklist = [record_id.search_vk_id for record_id in q_blacklist.all()]  # Делаем list comprehensions с существующими id в базе данных Blacklist
    for search in q_people.all():
        if search.search_vk_id not in id_list_blacklist:
            print(search.id, search.auser_id, search.search_vk_id, search.first_name, search.last_name, search.profile_link, search.first_likes, search.second_likes, search.third_likes)
    return True


def display_favorite(auser_id: int):
    q_favorite = session.query(Favourite).filter(Favourite.auser_id == auser_id) # Делаем запрос в базу данных Blacklist
    for search in q_favorite.all():
        print(search.id, search.auser_id, search.search_vk_id, search.first_name, search.last_name, search.profile_link, search.first_likes, search.second_likes, search.third_likes)
    return True



if __name__ == '__main__':
    # people_record_data(vk_methods.data_maker()) #Записываем в БД
    # delete_people_data(33647628)      #Удаляем из базы данных, необходимо ввести id удаляемого человека
    # blacklist_record_data(auser_id, 33647628)     #Заносим в черный список, первое значение это auser_id - id человека который ищет, второе значение это id человека которого мы нашли
    # delete_blacklist_data(auser_id, 33647628)     #Удаляем из черного списка первое значение это auser_id - id человека который ищет ("владельца черного списка", второе значение это id человека который в черном списке
    # favourites_record_data(auser_id, 33647628)  #Заносим в избранное, первое значение это auser_id - id человека который ищет, второе значение это id человека которого мы нашли
    # delete_favourites_data(auser_id, 33647628)  #Удаляем из избранного, первое значение это auser_id - id человека который ищет, второе значение это id человека которого мы нашли
    # print(join_people_favourites(auser_id, 33647628)) #Проверяем, есть ли пользователь в избранном, если функция возвращает None, значит человек не внесен в список избранных
    # print(join_people_blacklist(auser_id, 33647628))  #Проверяем, есть ли пользователь в черном списке, если функция возвращает None, значит человек не внесен в черный список
    # display_data_people(auser_id) # Отображаем список отобранных кандидатов с учетом проверки их отсутствия в черном списке
    display_favorite(auser_id) # Отображаем список избранных кандидатов















