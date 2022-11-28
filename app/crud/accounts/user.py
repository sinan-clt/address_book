from sqlalchemy.orm import Session
from app.schemas.accounts.user import *
from app.models.model import Users, OtpVerification
from app.models.model import *
import datetime as dtt



def create_customer(db: Session, customer: CustomerRegistrationBase, otp: int):
    users = db.query(Users).filter(Users.phone_number == customer.phone_number)
    count = users.count()

    if count == 0:
        db_user = Users(phone_number=customer.phone_number)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    else:
        db_user = users.first()

    generated_otp = OtpVerification(
        otp=otp, phone_number=customer.phone_number, user=db_user.id,created_at=dtt.datetime.utcnow() + dtt.timedelta(hours=5, minutes=30))
    db.add(generated_otp)
    db.commit()
    result = {"id": db_user.id,
              "phone_number": db_user.phone_number, "otp": otp}
    return result



def resend_otp_crud(db: Session, customer: CustomerRegistrationBase, otp: int):
    user = db.query(Users).filter(Users.phone_number ==
                                  customer.phone_number).first()
    if user:
        generated_otp = OtpVerification(
            otp=otp, phone_number=customer.phone_number, user=user.id, created_at=dtt.datetime.utcnow() + dtt.timedelta(hours=5, minutes=30) )
        db.add(generated_otp)
        db.commit()
        result = {"id": user.id,
                  "phone_number": user.phone_number, "otp": otp}
        return result
    return



def verify_otp(db: Session, credential: AuthDetails):
    user = db.query(Users).filter(
        Users.phone_number == credential.mobile).first()
    db.commit()
    return True, user



def get_user_details(db: Session, Authorize: str):
    user = db.query(Users).filter(Users.phone_number == Authorize).first()
    return user


def get_user_address_details_crud(db: Session, user: Users):
    address = db.query(UserAddress).filter(UserAddress.user_id == user.id).first()
    print(address)
    return  address