from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str
    email: EmailStr
    password: str

class UserInDB(User):
    hashed_password: str

class UserCreate(User):
    pass

class UserLogin(User):
    pass

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordUpdateRequest(BaseModel):
    token: str
    password: str