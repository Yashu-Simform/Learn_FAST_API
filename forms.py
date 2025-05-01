from fastapi import FastAPI, Body
from models import UserBase, UserRegistration, UserRegistrationResponse
from typing import Annotated

app = FastAPI()

app.post('user/register/')
def user_register(user_data: Annotated[UserRegistration, Body()]) -> UserRegistrationResponse:
    return user_data