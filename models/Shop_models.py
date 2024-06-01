from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_link import given_table
from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo

#변경 사항을 데이터베이스 파일에 새로 적용하고 싶다면
#alembic revision --autogenerate -m "메시지"
#alembic upgrade head

class Laptop_Models(given_table):
    __tablename__="Laptop shop"

    id=Column(Integer, primary_key=True, index=True)
    laptop_cpu=Column(String, nullable=False)
    laptop_gpu=Column(Text, nullable=False)
    laptop_display_inch=Column(Float, nullable=False)
    laptop_price=Column(Integer, nullable=False)
    created_at : Column(DateTime, default=lambda: datetime.now(ZoneInfo('UTC')))
#utcnow는 일부로 허용을 안해서, now를 씀
#반드시 Nullable=False인 거는 데이터가 들어가야 한다.


class Laptop_pydantic(BaseModel):
    laptop_cpu: str  #이런 식으로 필드(모델의 변수)에 형식을 매기는 것을 어토네이션이라 한다.
    laptop_gpu: str
    laptop_display_inch: float
    laptop_price: int
    upload_date: datetime

    class Config:
      orm_mode=True
      arbitrary_types_allowed=True


class common(given_table):
    __tablename__="Common Shoppers"

    id=Column(Integer, primary_key=True)
    user_name=Column(String, nullable=False)
    user_number_of_purchases=Column(Integer, nullable=False)
    money=Column(Integer, nullable=False)

class middle(given_table):
    __tablename__="Middle Class"

    id=Column(Integer, primary_key=True)
    user_name=Column(String, nullable=False)
    user_number_of_purchases=Column(Integer, nullable=False)
    money=Column(Integer, nullable=False)

class high(given_table):
    __tablename__="High Class"

    id=Column(Integer, primary_key=True)
    user_name=Column(String, nullable=False)
    user_number_of_purchases=Column(Integer, nullable=False)
    money=Column(Integer, nullable=False)    
