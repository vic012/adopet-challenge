from sqlalchemy import Column, String, Integer

from db.database import Base


class Tutors(Base):
    __tablename__ = "tutors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    hashed_password = Column(String)
    confirm_hashed_password = Column(String)
