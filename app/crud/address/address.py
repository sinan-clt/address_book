from sqlalchemy.orm import Session
from app.models.model import *
from app.schemas.address.address import *



def check_already_added(db: Session, user: int):
    return db.query(UserAddress).filter(UserAddress.user_id==user).all()


def create_address_crud(db: Session, address: AddressCreate, user: int):
    db_address = UserAddress(user_id=user, house_name=address.house_name, country=address.country,
                                state=address.state, district=address.district, zip_code=address.zip_code)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_user_address_info(db: Session, user_id: int):
    return db.query(UserAddress).filter(UserAddress.user_id==user_id).first()


def update_user_address(db: Session, user_address: AddressUpdate, user_id: int):
    print(user_id)

    cur_address = get_user_address_info(db, user_id)
    if cur_address:
        cur_address.house_name = user_address.house_name
        cur_address.country = user_address.country
        cur_address.state = user_address.state
        cur_address.district = user_address.district
        cur_address.zip_code = user_address.zip_code
        db.commit()



def get_user_address(db: Session, user: Users):
    return db.query(UserAddress).filter(UserAddress.user_id==user.id).first()


def get_user_address_details(db: Session, user_id: int):
    return db.query(UserAddress).filter(UserAddress.user_id==user_id).first()


def delete_address_crud(db: Session, user_id: int):
    cur_address = get_user_address_details(db, user_id)
    if cur_address:
        cur_address.is_deleted = True
        db.commit()