from pydantic import BaseModel, EmailStr, HttpUrl, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class BaseUser(BaseModel):
    username: str
    email: EmailStr | None = None


class User(BaseUser):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseUser):
    password: str


class BaseIngredient(BaseModel):
    name: str


class Ingredient(BaseIngredient):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class CreateIngredient(BaseIngredient):
    ...


class BaseRecipe(BaseModel):
    title: str
    description: str | None = None
    time_mins: int
    price: float
    link: HttpUrl
    tags: list = []
    ingredients: list[BaseIngredient] | None = None


class Recipe(BaseRecipe):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class CreateRecipe(BaseRecipe):
    ...
