import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class People(Base):
    __tablename__ = "people"

    id = sq.Column(sq.Integer, primary_key=True) #id
    auser_id = sq.Column(sq.Integer, nullable=False) #id человека которыый ищет
    search_vk_id = sq.Column(sq.Integer, nullable=False) #id людей которых мы ищем
    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    profile_link = sq.Column(sq.String(length=60), nullable=False)
    first_likes = sq.Column(sq.String(length=60), nullable=False)
    second_likes = sq.Column(sq.String(length=60), nullable=False)
    third_likes = sq.Column(sq.String(length=60), nullable=False)

class Blacklist(Base):
    __tablename__ = "blacklist"

    id = sq.Column(sq.Integer, primary_key=True) #id
    auser_id = sq.Column(sq.Integer, nullable=False) #id человека которыый ищет
    search_vk_id = sq.Column(sq.Integer, nullable=False) #id людей которых мы ищем
    # search_vk_id_people = sq.Column(sq.Integer, sq.ForeignKey("people.search_vk_id"), nullable=False)
    id_people = sq.Column(sq.Integer, sq.ForeignKey("people.id"), nullable=False)
    people = relationship(People, backref="blacklists")

class Favourite(Base):
    __tablename__ = "favourite"

    id = sq.Column(sq.Integer, primary_key=True)
    auser_id = sq.Column(sq.Integer, nullable=False) #id человека которыый ищет
    search_vk_id = sq.Column(sq.Integer, nullable=False) #id людей которых мы ищем
    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    profile_link = sq.Column(sq.String(length=60), nullable=False)
    first_likes = sq.Column(sq.String(length=60), nullable=False)
    second_likes = sq.Column(sq.String(length=60), nullable=False)
    third_likes = sq.Column(sq.String(length=60), nullable=False)
    # search_vk_id_people = sq.Column(sq.Integer, sq.ForeignKey("people.search_vk_id"), nullable=False)
    id_people = sq.Column(sq.Integer, sq.ForeignKey("people.id"), nullable=False)
    people = relationship(People, backref="favourites")


def create_tables(engine):
    Base.metadata.create_all(engine)