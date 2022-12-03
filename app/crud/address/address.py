from sqlalchemy.orm import Session
from app.models.model import *
from app.schemas.address.address import *
from sqlalchemy import text



def create_address_crud(db: Session, address: AddressCreate):
    db_address = Address(house_name=address.house_name, country=address.country, latitude=address.latitude, longitude=address.longitude,
                                state=address.state, district=address.district, zip_code=address.zip_code)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address(db: Session):
    return db.query(Address).filter(Address.is_deleted==False).all()
    

def get_address_by_id(db: Session, id: int):
    return db.query(Address).get(id)


def update_address_crud(db: Session, address: AddressUpdate, id: int):
    cur_address = get_address_by_id(db, id=id)
    cur_address.house_name = address.house_name
    cur_address.country = address.country
    cur_address.state = address.state
    cur_address.district = address.district
    cur_address.zip_code = address.zip_code
    cur_address.latitude = address.latitude
    cur_address.longitude = address.longitude

    db.commit()
    return cur_address


def delete_address_crud(db: Session, id: int):
    cur_address = get_address_by_id(db, id=id)
    cur_address.is_deleted = True
    db.commit()
    return cur_address
        

def get_address_by_lat_long(db: Session, address_search: AddressLocationSearch):
    select_query = text("""
    SELECT `address`.*, (6367*ACOS(COS(RADIANS(%f))
                *COS(RADIANS(`address`.`latitude`))*COS(RADIANS(`address`.`longitude`)-RADIANS(%f))
                +SIN(RADIANS(%f))*SIN(RADIANS(`address`.`latitude`))))
                AS distance FROM `address` WHERE address.is_deleted='0' HAVING
                distance < %f ORDER BY distance LIMIT %d
    """% (
            address_search.latitude,
            address_search.longitude,
            address_search.latitude,
        ))
    result = db.execute(select_query).fetchall()

    return result
