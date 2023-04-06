from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer

SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Tutors(Base):
    __tablename__ = "tutors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    hashed_password = Column(String)
    confirm_hashed_password = Column(String)

    def __str__(self):
        return self.email


class Shelter(Base):
    __tablename__ = "shelter"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)
    name_animal = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)

    def __str__(self):
        return self.name