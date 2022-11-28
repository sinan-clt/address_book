from fastapi import FastAPI, Depends, HTTPException, status, Response, Request, BackgroundTasks
from app.models.model import Base
from app.database.main import engine, SessionLocal
from sqlalchemy.orm import Session
from app.crud.accounts.user import *
from app.crud.address.address import *
from app.schemas.accounts.user import *
from app.schemas.address.address import *
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import random
import math


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Settings(BaseModel):
    authjwt_secret_key:str="secret"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response



# API'S STARTING FROM HERE ***************

# verifying mobile_number by generating_otp ************
def generateOTP():
    digits = "0123456789"
    OTP = ""
    print("OTP Generation")
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return "1234"


# user_registration ************
@app.post("/usercreate", status_code=200)
async def create_user(customer: CustomerRegistrationBase, db: Session = Depends(get_db)):
    otp = generateOTP()
    customer = create_customer(db, customer, otp)
    return customer


# resend_otp by using mobile_number ************
@app.post("/resendOTP", status_code=200)
async def resend_otp(customer: CustomerRegistrationBase, db: Session = Depends(get_db)):
    otp = generateOTP()
    customer = resend_otp_crud(db, customer, otp)
    if customer:
        return customer
    else:
        raise HTTPException(status_code=401, detail='Phone number not exist')


# verify_user by using mobile_number and otp ************
@app.post("/verifyotp")
def login(auth_details: AuthDetails, Authorize:AuthJWT=Depends(), db: Session = Depends(get_db)):
    user_authenticated, user = verify_otp(db, credential=auth_details)
    if user_authenticated:
        access_token=Authorize.create_access_token(auth_details.mobile, expires_time=85000)
        refresh_token=Authorize.create_refresh_token(auth_details.mobile)
        resdata = {'phone_number': user.phone_number ,
                        'access_token': access_token, 'refresh_token': refresh_token}
        raise HTTPException(status_code=200, detail=resdata)
    else:
        raise HTTPException(status_code=401, detail='Invalid otp')


# getting details of logged_in user ************
@app.get("/getuserdetails", response_model=UserDetailsBase, status_code=status.HTTP_200_OK)
async def getUserDetails(Authorize:AuthJWT=Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    user_details = Authorize.get_jwt_subject()
    users = get_user_details(db, user_details)
    address =  get_user_address_details_crud(db, users)
    return {"user": users, "address": address}



# creating the address of the user ************
@app.post("/createAddress")
async def create_user_address(adddress: AddressCreate, db: Session = Depends(get_db), Authorize: AuthJWT=Depends()):
    Authorize.jwt_required()
    auth = Authorize.get_jwt_subject()
    user = get_user_details(db, auth)
    if len(check_already_added(db, user.id)) > 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail="address already added !")
    create_address_crud(db, adddress, user.id)
    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail={"status":"address added successfully"})


# getting the address of the user ************
@app.get("/getUserAddress", response_model=AddressBase, status_code=status.HTTP_200_OK)
async def getUserAddress(db: Session = Depends(get_db),Authorize:AuthJWT=Depends(), ):
    Authorize.jwt_required()
    auth = Authorize.get_jwt_subject()
    user = get_user_details(db, auth)
    address = get_user_address(db, user)
    return address


# uodating the address of the user ************
@app.put("/userAddressUpdate")
async def user_address_update(address: AddressUpdate, db: Session = Depends(get_db), Authorize: AuthJWT=Depends()):
    Authorize.jwt_required()
    auth = Authorize.get_jwt_subject()
    user = get_user_details(db, auth)

    if address is not None:
        update_user_address(db, address, user.id)

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail={"status":"address updated successfully"})



# deleting the address of the user ************
@app.post("/deleteAddress")
async def delete_address(db: Session = Depends(get_db), Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()
    auth = Authorize.get_jwt_subject()
    user = get_user_details(db,auth)
  
    delete_address_crud(db, user.id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="removed from shortlist")
   








#*************** or creating new_access_token ********************************

# @app.get('/new_token')
# def create_new_token(Authorize:AuthJWT=Depends()):
#     try:
#         Authorize.jwt_refresh_token_required()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
#     current_user=Authorize.get_jwt_subject()
#     access_token=Authorize.create_access_token(subject=current_user, expires_time=28800)
#     return {"new_access_token":access_token}
