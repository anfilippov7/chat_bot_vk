import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models import create_tables

load_dotenv()

# Предварительно нужно создать базу данных в командной строке операционной системы командой: createdb -U postgres chat_bot_vk

# DSN = 'postgresql://postgres:1234@localhost:5432/chat_bot_vk'

# В переменной окружения операционной системы прописываем переменную DSN со значением 'postgresql://postgres:1234@localhost:5432/chat_bot_vk'
# где 1234 это пароль от базы данных (у каждого разработчика может отличаться)

DSN = os.getenv("DSN")

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.close()


# if __name__ == '__main__':




