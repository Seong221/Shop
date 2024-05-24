from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database.db_link import given_table

#변경 사항을 데이터베이스 파일에 새로 적용하고 싶다면
#alembic revision --autogenerate -m "메시지"
#alembic upgrade head

class Pistol_Armory(given_table):
    __tablename__="Pistol Armory"

    id=Column(Integer, primary_key=True)
    pistol_type=Column(String, nullable=False)
    pistol_name=Column(Text, nullable=False)
    upload_date=Column(DateTime, default=datetime.datetime.now(), nullable=False)
#utcnow는 일부로 허용을 안해서, now를 씀
#반드시 Nullable=False인 거는 데이터가 들어가야 한다.

class Users(given_table):
    __tablename__="Pistol Users"

    id=Column(Integer, primary_key=True)
    user_name=Column(String, ForeignKey("Pistol Armory.pistol_name"))

    prevent_Unbound=relationship("Pistol_Armory", backref="users",uselist=False)   