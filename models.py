from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table, LargeBinary
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, unique=True)
    username = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)

    recipes = relationship('Recipe', back_populates='user')
    tags = relationship('Tag', back_populates='user')
    ingredients = relationship('Ingredient', back_populates='user')


ingredients_recipes = Table(
    "ingredients_recipes",
    Base.metadata,
    Column("ingredient_id", ForeignKey("Ingredients.id"), primary_key=True),
    Column("recipe_id", ForeignKey("Recipes.id"), primary_key=True),
)

tags_recipes = Table(
    "tags_recipes",
    Base.metadata,
    Column("tag_id", ForeignKey("Tags.id"), primary_key=True),
    Column("recipe_id", ForeignKey("Recipes.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = 'Tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship('User', back_populates='tags')

    recipes = relationship(
        "Recipe", secondary=tags_recipes, back_populates="tags"
    )


class Ingredient(Base):
    __tablename__ = 'Ingredients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship('User', back_populates='ingredients')

    recipes = relationship(
        "Recipe", secondary=ingredients_recipes, back_populates="ingredients"
    )


class Recipe(Base):
    __tablename__ = 'Recipes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    time_mins = Column(Integer)
    price = Column(Float)
    link = Column(String)
    image = Column(LargeBinary)

    tags = relationship(
        "Tag", secondary=tags_recipes, back_populates="recipes"
    )
    ingredients = relationship(
        "Ingredient", secondary=ingredients_recipes, back_populates="recipes"
    )
    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship('User', back_populates='recipes')
