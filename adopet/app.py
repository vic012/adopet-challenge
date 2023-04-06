from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
import validators


aplication = FastAPI(
	title="Adopet API",
	description="API que conecta Pessoas apaixonadas por pets"
)

#Session
def get_db():
	db = models.SessionLocal()
	try:
		yield db
	finally:
		db.close()

@aplication.post("/tutores/", response_model = schemas.Tutors, tags=["Criar um novo tutor"])
def criar_tutor(tutor: schemas.TutorsCreate, db: Session = Depends(get_db)):
	tutor = crud.create_tutors(db=db, tutor=tutor)
	if tutor.get("error"):
		raise HTTPException(status_code=400, detail=tutor["error"])
	return tutor["result"]

@aplication.get("/tutores/", response_model = List[schemas.Tutors], tags=["Filtrar todos os tutores"])
def pesquisar_todos_tutores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	tutors = crud.get_tutors(db, skip=skip, limit=limit)
	if not tutors:
		raise HTTPException(status_code=400, detail="Não existe nenhum tutor cadastrado")	
	return tutors

@aplication.get("/tutores/{tutor_id}", response_model = schemas.GetTutorsById, tags=["Filtrar um tutor pelo ID"])
def pesquisar_tutor_pelo_id(tutor_id: int, db: Session = Depends(get_db)):
	tutor = crud.get_tutor_by_id(db, tutor_id=tutor_id)
	if not tutor:
		raise HTTPException(status_code=400, detail="Não encontrado")
	return tutor

@aplication.put(
	"/tutores/{tutor_id}", #response_model = schemas.Tutors,
	tags=["Atualizar um tutor a partir do ID"]
)
def atualizar_tutor(tutor_id: int, tutor: schemas.TutorsCreate, db: Session = Depends(get_db)):
	tutor = crud.update_tutors(db, tutor_id=tutor_id, tutor=tutor)
	if tutor.get("error"):
		raise HTTPException(status_code=400, detail=tutor["error"])
	return tutor["result"]

@aplication.patch("/tutores/{tutor_id}", tags=["Atualizar campos específicaos de um tutor a partir do ID"])
def atualizar_tutor_parcialmente(tutor_id: int, tutor: schemas.TutorsUpdate, db: Session = Depends(get_db)):
	tutor = crud.update_partial_tutors(db, tutor_id=tutor_id, tutor=tutor)
	if tutor.get("error"):
		raise HTTPException(status_code=400, detail=tutor["error"])
	return tutor["result"]

@aplication.delete("/tutores/{tutor_id}", tags=["Deletar um tutor a partir do ID"])
def deletar_tutor(tutor_id: int, db: Session = Depends(get_db)):
	tutor = crud.delete_tutors(db, tutor_id=tutor_id)
	if tutor.get("error"):
		raise HTTPException(status_code=400, detail=tutor["error"])
	return tutor["result"]

