from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

import CRUD
import jwt_token
import schemas
from database import get_db

users_router = APIRouter(prefix='/users', tags=['User'],
                         dependencies=[Depends(jwt_token.get_current_active_user)])


@users_router.delete('/delete')
async def delete_current_user(db: Session = Depends(get_db),
                              current_user: schemas.User = Depends(jwt_token.get_current_active_user)):
    db.delete(current_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@users_router.put('/update')
async def update_current_user(user_schema: schemas.UserCreate,
                              db: Session = Depends(get_db),
                              current_user: schemas.User = Depends(jwt_token.get_current_active_user)):
    current_user.username = user_schema.username
    current_user.email = user_schema.email
    current_user.hashed_password = jwt_token.get_password_hash(user_schema.password)
    db.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)


@users_router.get('/me', response_model=schemas.User)
async def get_current_user(
        current_user: schemas.User = Depends(jwt_token.get_current_active_user)):
    return current_user


@users_router.get('/', response_model=list[schemas.User])
async def get_all_users(db: Session = Depends(get_db),
                        skip: int = 0,
                        limit: int = 100):
    return CRUD.get_users(db=db, skip=skip, limit=limit)


@users_router.get('/{user_id}', response_model=schemas.User)
async def get_user_by_id(user_id: int,
                         db: Session = Depends(get_db)):
    return CRUD.get_user(db, user_id)
