from fastapi import APIRouter
from fastapi import Depends, status, Response
from sqlalchemy.orm import Session

import CRUD
import jwt_token
import schemas
from database import get_db

recipe_router = APIRouter(prefix='/recipes', tags=['Recipe'])


@recipe_router.post('/create')
async def create_new_recipe(
        recipe: schemas.CreateRecipe,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt_token.get_current_active_user)

):
    CRUD.create_recipe(db=db, user=current_user, recipe=recipe)
    return Response(status_code=status.HTTP_201_CREATED)


@recipe_router.get('/', response_model=list[schemas.Recipe])
async def get_all_recipes(my_recipes: bool,
                          db: Session = Depends(get_db),
                          current_user: schemas.User = Depends(jwt_token.get_current_active_user),
                          ):
    return CRUD.get_recipes(db, my_recipes, current_user)
