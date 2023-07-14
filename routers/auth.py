from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
import CRUD
import jwt_token
import schemas
from database import get_db

auth_router = APIRouter(prefix='/auth', tags=['Registration and Authorization'])


@auth_router.post('/create')
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = CRUD.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    jwt_token.create_user(db=db, user=user)
    return Response(status_code=status.HTTP_201_CREATED)


@auth_router.post('/token', response_model=schemas.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = jwt_token.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=jwt_token.expire_minutes)
    access_token = jwt_token.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
