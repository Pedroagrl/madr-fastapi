from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select

from sqlalchemy.orm import Session
from madr.models import User
from madr.schemas import Message, UserDB, UserList, UserPublic, UserSchema

from madr.database import get_session

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code = HTTPStatus.BAD_REQUEST,
                detail = 'Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code = HTTPStatus.BAD_REQUEST,
                detail = 'Email already exists',
            )
            
    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    #Um recurso para limitar e mostrar certa quantidade de registros.
    limit: int = 10,
    #Dita de onde vai começar a contar o limit
    skip: int = 0,
    session: Session = Depends(get_session)
    
    ):
    user = session.scalars(
        select(User).limit(limit).offset(skip)
        )
    return {'users': user}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPException.NOT_FOUND, detail='User not found'
        )
    
    db_user.email == user.email
    db_user.username == user.username
    db_user.password == user.password

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPException.NOT_FOUND, detail='User not found'
        )
    session.delete(db_user)
    session.commit()

    return{'message': 'User deleted'}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user__exercicio(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return database[user_id - 1]
