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
        q_people = session.query(People) #Делаем запрос в базу данных People
        id_list = [record_id.id for record_id in q_people.all()] #Делаем list comprehensions с существующими id в базе данных People
        for record in data:
            if record['id'] not in id_list: #Если id в выборке функции vk_methods.data_maker() отсутствует в базе данных (в list comprehensions), делаем запись в БД
                session.add(People(id=record['id'], first_name=record['first_name'], last_name=record['last_name'],
                            profile_link=record['profile_link'], first_likes=record['first_likes'],
                            second_likes=record['second_likes'], third_likes=record['third_likes']))
                session.commit()
        # print(f'Данные записаны в базу данных people!')
        return True
    except Exception as ex:
        # print(f'Все данные уже были загружены в базу данных!', ex)
        return False, ex


def delete_people_data(id_delete: int) -> 'deleting an entry':
    # Удаляем запись из базы данных People
    try:
        q_blacklist = session.query(Blacklist) #Делаем запрос в базу данных Blacklist
        q_favourite = session.query(Favourite) #Делаем запрос в базу данных Favourite
        id_list_blacklist = [record_id.id for record_id in q_blacklist.all()] #Делаем list comprehensions с существующими id в базе данных Blacklist
        id_list_favourite = [record_id.id for record_id in q_favourite.all()] #Делаем list comprehensions с существующими id в базе данных Favourite
        if id_delete not in id_list_blacklist and id_delete not in id_list_favourite:
            session.query(People).filter(People.id == id_delete).delete()
            session.commit()
            # print(f'Данные удалены из базы данных people!')
        elif id_delete in id_list_blacklist:
            print(f'Удалите id {id_delete} из черного списка!')
        elif id_delete in id_list_favourite:
            print(f'Удалите id {id_delete} из избранного списка!')
        return True
    except Exception as ex:
        # print(f'Данной записи нет в базе данных people!', ex)
        return False, ex


def blacklist_record_data(id_blacklist: int) -> 'record blacklist SQL':
    # Записываем данные в таблицу Blacklist базы данных
    try:
        q_people = session.query(People).filter(People.id == id_blacklist)
        q_blacklist = session.query(Blacklist) #Делаем запрос в базу данных Blacklist
        id_list_blacklist = [record_id.id_people for record_id in q_blacklist.all()] #Делаем list comprehensions с существующими id в базе данных Blacklist
        if id_blacklist not in id_list_blacklist:
            for record_id in q_people.all():
                session.add(Blacklist(id_people=record_id.id))
            session.commit()
            print(f'Данные записаны в базу данных blacklist!')
        else:
            print('Человек уже внесен в базу данных!')
        return True
    except Exception as ex:
        # print(f'Все или часть данных уже были загружены в базу данных blacklist!', ex)
        return False, ex

def delete_blacklist_data(id_delete: int) -> 'deleting an entry':
    # Удаляем запись из базы данных Blacklist
    try:
        session.query(Blacklist).filter(Blacklist.id_people == id_delete).delete()
        session.commit()
        print(f'Данные удалены из базы данных blacklist!')
        return True
    except Exception as ex:
        print(f'Данной записи нет в базе данных blacklist!', ex)
        return False, ex


def favourites_record_data(id_favourite: int) -> 'record favourite SQL':
    # Записываем данные в таблицу Favourite базы данных
    try:
        q_people = session.query(People).filter(People.id == id_favourite)
        q_favourite = session.query(Favourite) #Делаем запрос в базу данных Favourite
        id_list_favourite = [record_id.id_people for record_id in q_favourite.all()] #Делаем list comprehensions с существующими id в базе данных Blacklist
        if id_favourite not in id_list_favourite:
            for record_id in q_people.all():
                session.add(Favourite(id_people=record_id.id))
            session.commit()
            print(f'Данные записаны в базу данных favourites!')
        else:
            print('Человек уже внесен в базу данных!')
        return True
    except Exception as ex:
        # print(f'Все или часть данных уже были загружены в базу данных favourites!', ex)
        return False, ex


def delete_favourites_data(id_delete: int) -> 'deleting an entry':
    # Удаляем запись из базы данных Favourite
    try:
        session.query(Favourite).filter(Favourite.id_people == id_delete).delete()
        session.commit()
        print(f'Данные удалены из базы данных favourites!')
        return True
    except Exception as ex:
        print(f'Данной записи нет в базе данных favourites!', ex)
        return False, ex


def join_people_favourites(id_vk):
    #Джойним таблицы people и favourite
    query = session.query(People, Favourite).filter(People.id == id_vk)
    query = query.join(Favourite, Favourite.id_people == People.id)
    records = query.all()
    for people, favourite in records:
        return people.id, favourite.id_people


def join_people_blacklist(id_vk):
    #Джойним таблицы people и blacklist
    query = session.query(People, Blacklist).filter(People.id == id_vk)
    query = query.join(Blacklist, Blacklist.id_people == People.id)
    records = query.all()
    for people, blacklist in records:
        return people.id, blacklist.id_people

session.close()

if __name__ == '__main__':
    people_record_data(vk_methods.data_maker()) #Записываем в БД
    # delete_people_data(1297960)      #Удаляем из базы данных, необходимо ввести id удаляемого человека
    # blacklist_record_data(25919734)     #Заносим в черный список по id vk
    # delete_blacklist_data(33647628)     #Удаляем из черного списка по id vk
    # favourites_record_data(33647628)  #Заносим в избранное по id vk
    # delete_favourites_data(33647628)  #Удаляем из избранного по id vk
    # join_people_favourites(419794645) #Проверяем, есть ли пользователь в избранном, если функция возвращает None, значит человек не внесен в список избранных
    # join_people_blacklist(419794645)  #Проверяем, есть ли пользователь в черном списке, если функция возвращает None, значит человек не внесен в черный список

















