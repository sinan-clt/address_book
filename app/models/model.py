from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.main import Base
import datetime as dtt
from sqlalchemy.orm import backref
import datetime
from datetime import datetime




class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    house_name = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    district = Column(String(50), nullable=True)
    zip_code = Column(Integer, nullable=True)
    longitude = Column(String(20), nullable=True)
    latitude = Column(String(20), nullable=True)
    is_deleted = Column(Boolean(), default=False)
    create_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)