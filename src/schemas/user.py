from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str
    email: EmailStr
    password: str

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str