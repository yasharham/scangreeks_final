from fastapi import Form
from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    Client_id: str
    Username: str
    Role: str
    Email: str
    Mobile_no: str
    Password: str
    # otp: Optional[int] = Form()


class UserLogin(BaseModel):
    Client_id: str
    Password: str

# class showUser(BaseModel):
#     name:str
#     class Config():
#         orm_mode = True

class Show(BaseModel):
    name : str
    email: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    role: str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[int] = None


class Features(BaseModel):
    name: str
    class Config:
        orm_mode = True

class Plan(BaseModel):
    plan_name : str
    price : Optional[int]
    features : Optional[List]

class Updateplan(BaseModel):
    price : Optional[int]
    features : Optional[List]

# class showFeature(features):
#
#     class Config:
#         orm_mode = True

class Pancard(BaseModel):
    number:str


class Payment(BaseModel):
    # username : str
    # plan_name : str
    amount: int
    validity : str
    # date:datetime

class GetMaster(BaseModel):
    name:str
    security:float
    stamp_duty:float
    turnover:float
    SEBI:float
    clearing:float
    other_charges:float


class BillData(BaseModel):
    date:str
    segment:str

class billTradeData(BaseModel):
    segment:str
    date:str
    symbol:str

class JvData(BaseModel):
    date:str
    narration:str
    entry:str
    amount:float

class Expense(BaseModel):
    date:str

class ClosingPostion(BaseModel):
    date:str


    # narration:str
    # entry:str
    # amount:float


class dateRange(BaseModel):
    startDate:str
    endDate:str