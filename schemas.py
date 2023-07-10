from pydantic import BaseModel, EmailStr


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
