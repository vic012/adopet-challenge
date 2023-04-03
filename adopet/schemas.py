from typing import List, Union

from pydantic import BaseModel


class TutorsBase(BaseModel):
    email: str
    name: str


class TutorsCreate(TutorsBase):
    email: str
    name: str
    hashed_password: str
    confirm_hashed_password: str


class TutorsUpdate(BaseModel):
    email: str = None
    name: str = None
    hashed_password: str = None
    confirm_hashed_password: str = None


class Tutors(TutorsBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class GetTutorsById(TutorsBase):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
