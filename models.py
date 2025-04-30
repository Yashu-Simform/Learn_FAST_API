from pydantic import BaseModel, EmailStr, Field

class BankClient(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(
        default=None,
        min_length= 8,
        max_length=12,
    )
    name: str