from pydantic import BaseModel
from typing import Optional



class AddressCreate(BaseModel):
    house_name: str
    country: str
    state: str
    district: str
    zip_code: int

    class Config:
        orm_mode = True


class AddressUpdate(BaseModel):
    house_name: str
    country: str
    state: str
    district: str
    zip_code: int

    class Config:
        orm_mode = True



class AddressBase(BaseModel):
    house_name: str
    country: str
    state: str
    district: str
    zip_code: int
    is_deleted:bool

    class Config:
        orm_mode = True


