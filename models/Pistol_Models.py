from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.db_link import given_table

class Pistol_Armory(given_table):
    __tablename__="Pistol Armory"

    id=Column(Integer, primary_key=True)
    pistol_type=Column(String, nullable=False)
    pistol_name=Column(Text, nullable=False)
    upload_date=Column(DateTime, nullable=False)


class Users(given_table):
    __tablename__="Pistol Users"

    id=Column(Integer, primary_key=True)
    user_name=Column(String, ForeignKey("Pistol Armory.pistol_name"))
    