from pydantic import BaseModel


class UserSignUp(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class UserSignIn(BaseModel):
    email: str
    password: str
