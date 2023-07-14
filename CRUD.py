from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_recipe(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def get_recipes(db: Session, my_recipes: bool, user):
    if my_recipes:
        return db.query(models.Recipe).filter(models.Recipe.user_id == user.id).all()
    return db.query(models.Recipe).all()


def create_recipe(db: Session, user, recipe: schemas.CreateRecipe):
    recipe_data = recipe.dict()
    ingredient_data = recipe_data.pop('ingredients', None)
    db_recipe = models.Recipe(**recipe_data, user_id=user.id)
    db.add(db_recipe)
    db.commit()
    for ingredient in ingredient_data:
        db_ingredient = models.Ingredient(**ingredient, user_id=user.id)
        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)
    return db_recipe
