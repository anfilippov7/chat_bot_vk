import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Town(Base):
    __tablename__ = "town"

    id = sq.Column(sq.Integer, primary_key=True)
    town = sq.Column(sq.String(length=40), nullable=False)

class Gender(Base):
    __tablename__ = "gender"

    id = sq.Column(sq.Integer, primary_key=True)
    gender = sq.Column(sq.String(length=40), unique=True, nullable=False)

class Age(Base):
    __tablename__ = "age"

    id = sq.Column(sq.Integer, primary_key=True)
    age = sq.Column(sq.String(length=40), nullable=False)

class People(Base):
    __tablename__ = "people"

    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=40), nullable=False)
    last_name = sq.Column(sq.String(length=40), nullable=False)
    id_age = sq.Column(sq.Integer, sq.ForeignKey("age.id"), nullable=False)
    id_gender = sq.Column(sq.Integer, sq.ForeignKey("gender.id"), nullable=False)
    id_town = sq.Column(sq.Integer, sq.ForeignKey("town.id"), nullable=False)
    town = relationship(Town, backref="stocks")
    gender = relationship(Gender, backref="stocks")
    age = relationship(Age, backref="stocks")



def create_tables(engine):
    Base.metadata.create_all(engine)




























