from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from app.models.model import Base
from app.database.main import engine, SessionLocal
from sqlalchemy.orm import Session
from app.crud.address.address import *
from app.schemas.address.address import *
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List


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

# creating the address ************
@app.post("/createAddress")
async def create_address(adddress: AddressCreate, db: Session = Depends(get_db)):
    create_address_crud(db, adddress)
    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail={"status":"address added successfully"})


# getting the address ************
@app.get("/getAddress", status_code=status.HTTP_200_OK)
async def getAddress(db: Session = Depends(get_db)):
    address = get_address(db)
    return address


# # updating the address ************
@app.put('/AddressUpdate/{address_id}', status_code=status.HTTP_200_OK)
async def update_address(address_id: int, address: AddressUpdate, response: Response, db: Session = Depends(get_db)):
    is_address_exist = get_address_by_id(db, id=address_id)
    if is_address_exist:
        update_address_crud(db=db, address=address, id=address_id)
        return {"detail": "address updated successfully"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="address doesn't exist")


# # deleting the address ************
@app.delete('/deleteAddress/{address_id}', status_code=status.HTTP_200_OK)
def delete_address(address_id: int, response: Response, db: Session = Depends(get_db)):
    is_address_exist = get_address_by_id(db, id=address_id)
    if is_address_exist:
        delete_address_crud(db, address_id)
        return {"detail": "address deleted succesfully"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="address details doesn't exist")


# # get address by coordinates ************
@app.post("/getNearByAddress", response_model=List[AddressBase], status_code=status.HTTP_200_OK)
async def get_near_by_address(address_search: AddressLocationSearch, db: Session = Depends(get_db)):
    address = get_address_by_lat_long(db, address_search)
    return address