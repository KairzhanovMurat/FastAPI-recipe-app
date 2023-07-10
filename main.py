from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
import jwt_token
import schemas, CRUD, models
from database import get_db, engine
import uvicorn

app = FastAPI(docs_url='/')

models.Base.metadata.create_all(bind=engine)


@app.post("/token", response_model=schemas.Token, tags=['Token'])
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


@app.post('/users/create', tags=['User'])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = CRUD.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    jwt_token.create_user(db=db, user=user)
    return Response(status_code=status.HTTP_201_CREATED)


@app.delete('/users/delete', tags=['User'])
async def delete_current_user(db: Session = Depends(get_db),
                              current_user: schemas.User = Depends(jwt_token.get_current_active_user)):
    db.delete(current_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/users/update', tags=['User'])
async def update_current_user(user_schema: schemas.UserCreate,
                              db: Session = Depends(get_db),
                              current_user: schemas.User = Depends(jwt_token.get_current_active_user),
                              ):
    current_user.username = user_schema.username
    current_user.email = user_schema.email
    current_user.hashed_password = jwt_token.get_password_hash(user_schema.password)
    db.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)


@app.get("/users/me/", response_model=schemas.User, tags=['User'])
async def get_current_user(
        current_user: schemas.User = Depends(jwt_token.get_current_active_user)
):
    return current_user


@app.get('/users/', response_model=list[schemas.User], tags=['User'])
async def get_all_users(db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(jwt_token.get_current_active_user),
                        skip: int = 0,
                        limit: int = 100):
    return CRUD.get_users(db=db, skip=skip, limit=limit)


@app.get('/users/{user_id}', response_model=schemas.User, tags=['User'])
async def get_user_by_id(user_id: int,
                         db: Session = Depends(get_db),
                         current_user: schemas.User = Depends(jwt_token.get_current_active_user)
                         ):
    return CRUD.get_user(db, user_id)





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
