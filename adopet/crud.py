from sqlalchemy.orm import Session
import models, schemas, validators
from fastapi.encoders import jsonable_encoder
import bcrypt


def get_tutors(db: Session, skip: int, limit: int):
	return db.query(models.Tutors).all()

def get_tutor_by_id(db: Session, tutor_id: int):
	return db.query(models.Tutors).filter(models.Tutors.id == tutor_id).first()

def get_tutors_by_email(db: Session, tutors_email: str):
	return db.query(models.Tutors).filter(models.Tutors.email == tutors_email).first()

def create_tutors(db: Session, tutor: schemas.TutorsCreate):
	email = tutor.email
	valid_email = validators.check(email)
	if not valid_email:
		return {"error": "Este e-mail é inválido"}

	tutor_exists = get_tutors_by_email(db, tutors_email=tutor.email)
	if tutor_exists:
		return {"error": "Este e-mail já está sendo usado por outro usuário"}

	valid_password = validators.valid_password(
		tutor.hashed_password,
		tutor.confirm_hashed_password
	)
	if not valid_password:
		return {"error": "As senhas não são iguais"}

	salt = bcrypt.gensalt()
	hashed = bcrypt.hashpw(tutor.hashed_password.encode('ascii'), salt)
	tutor.hashed_password = hashed
	tutor.confirm_hashed_password = hashed
	tutors_created = models.Tutors(
		email = tutor.email,
		name = tutor.name,
		hashed_password = tutor.hashed_password,
		confirm_hashed_password= tutor.hashed_password
	)
	db.add(tutors_created)
	db.commit()
	db.refresh(tutors_created)
	return {"result": tutors_created}

def update_tutors(db: Session, tutor_id: int, tutor: schemas.TutorsCreate):
	tutor_object = get_tutor_by_id(db, tutor_id=tutor_id)
	if not tutor_object:
		return {"error": "Tutor não encontrado"}
	valid_password = validators.valid_password(
		tutor.hashed_password,
		tutor.confirm_hashed_password
	)
	if not valid_password:
		return {"error": "As senhas não são iguais"}
	salt = bcrypt.gensalt()
	hashed = bcrypt.hashpw(tutor.hashed_password.encode('ascii'), salt)

	valid_email = validators.check(tutor.email)
	if not valid_email:
		return {"error": "Este e-mail é inválido"}

	tutor_object.email = tutor.email
	tutor_object.name = tutor.name
	tutor_object.hashed_password = hashed
	tutor_object.confirm_hashed_password = hashed
	db.add(tutor_object)
	db.commit()
	db.refresh(tutor_object)
	return {"result": tutor_object}

def update_partial_tutors(db: Session, tutor_id: int, tutor: schemas.TutorsCreate):
	tutor_object = db.query(models.Tutors).filter(models.Tutors.id == tutor_id)
	if not tutor_object.first():
		return {"error": "Tutor não encontrado"}
	object_data = tutor.dict(exclude_unset=True)

	#Validará se o campo atualizado for o e-mail
	if object_data.get("email"):
		valid_email = validators.check(tutor.email)
		if not valid_email:
			return {"error": "Este e-mail é inválido"}

	#Se o campo que se deseja atualizar envolver senha
	if object_data.get("hashed_password") or object_data.get("confirm_hashed_password"):
		#Caso os dois campos de senha não tenham sido enviados
		if object_data.get("hashed_password") and not object_data.get("confirm_hashed_password")\
		or not object_data.get("hashed_password") and object_data.get("confirm_hashed_password"):
			return {"error": "Informe os campos 'hashed_password' e 'confirm_hashed_password'"}
	
	#Validará as senhas
	if object_data.get("hashed_password") and object_data.get("confirm_hashed_password"):
		valid_password = validators.valid_password(
			tutor.hashed_password,
			tutor.confirm_hashed_password
		)
		if not valid_password:
			return {"error": "As senhas não são iguais"}
		salt = bcrypt.gensalt()
		hashed = bcrypt.hashpw(object_data["hashed_password"].encode('ascii'), salt)
		object_data["hashed_password"] = hashed
		object_data["confirm_hashed_password"] = hashed

	object_data = jsonable_encoder(object_data)
	tutor_object.update(object_data)
	db.commit()
	return {"result": object_data}

def delete_tutors(db: Session, tutor_id: int):
	tutor = get_tutor_by_id(db, tutor_id=tutor_id)
	if not tutor:
		return {"error": "Não encontrado"}
	db.delete(tutor)
	db.commit()
	return {"result": "Tutor deletado com sucesso"}

