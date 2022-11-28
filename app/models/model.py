from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.main import Base
import datetime as dtt
from sqlalchemy.orm import backref
import datetime
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(15))
    otps = relationship("OtpVerification")
    create_at = Column(DateTime(timezone=True), default=dtt.datetime.utcnow() + dtt.timedelta(hours=5, minutes=30))
    updated_at = Column(DateTime(timezone=True), onupdate=dtt.datetime.utcnow() + dtt.timedelta(hours=5, minutes=30))


class OtpVerification(Base):
    __tablename__ = 'otp_verification'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(15))
    otp = Column(String(256))
    user = Column(Integer, ForeignKey('users.id'))
    is_verified = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), default=dtt.datetime.utcnow() + dtt.timedelta(hours=5, minutes=30))


class UserAddress(Base):
    __tablename__ = 'user_address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    house_name = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    district = Column(String(50), nullable=True)
    zip_code = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("Users", backref=backref("user_address_details", uselist=False))
    is_deleted = Column(Boolean(), default=False)
    create_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)