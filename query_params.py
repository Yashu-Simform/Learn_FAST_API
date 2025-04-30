from fastapi import FastAPI

from pydantic import BaseModel


# Use this as query params
class Transaction(BaseModel):
    model_config = {"extra": "forbid"}

    transaction_id: int
    from_acc: str | None
    to_acc: str | None
    amount: int | None
