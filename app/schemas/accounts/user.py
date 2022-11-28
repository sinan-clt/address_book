from pydantic import BaseModel
from typing import  Optional
from app.models.model import *



class AuthDetails(BaseModel):
    mobile: str
    otp: str

    
class CustomersBase(BaseModel):
    id: int
    username: Optional[str]
    phone_number: str


    class Config:
        orm_mode = True


class CustomerRegistrationBase(BaseModel):
    phone_number: str

    class Config:
        orm_mode = True



class UsersBase(BaseModel):
    id: int
    phone_number: str

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    house_name: str
    country: str
    state: str
    district: str
    zip_code: int
    is_deleted: bool

    class Config:
        orm_mode = True



class UserDetailsBase(BaseModel):
    user : Optional[UsersBase]
    address: Optional[AddressBase]



    class Config:
        orm_mode = True