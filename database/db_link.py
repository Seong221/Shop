from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_file_save_place="sqlite:///./caution.db"

engine=create_engine(
    db_file_save_place, connect_args={"check_same_thread":False}
)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

given_table=declarative_base()