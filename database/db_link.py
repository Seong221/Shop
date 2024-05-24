from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_file_save_place="sqlite:///./caution.db"

engine=create_engine(
    db_file_save_place, connect_args={"check_same_thread":False}
)

given_table=declarative_base()

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)




#데이터베이스에 세션을 연결하고, 연결 세션을 통해 데이터베이스에 데이터 저장.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
