from fastapi import FastAPI, Form, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from models.Shop_models import Laptop_Models, Laptop_pydantic, Shoppers, Shopper_pydantic
from fastapi.templating import Jinja2Templates
from database.db_link import get_db, given_table, engine
from sqlalchemy.orm import Session
import bcrypt


from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta, timezone
###API 호출, 프론트엔드에서 버튼 입력 -> DB에 저장, 만든 사이트를 aws에서 서비스하고 그 IP로 접속이 되는 지 확인하는 게 중요###


second_test=FastAPI()
#session=Session() 이 부분 때문에 오류가 난 듯합니다. session은 의존성 주입을 사용해야 된다고 하더군요. 
#이렇게 session 객체를 만들고 함수 안에 db대신 썼더니 UnBound 오류가 난 듯 합니다. 

given_table.metadata.create_all(bind=engine) #데이터베이스에 테이블 생성이라는 의미

templates=Jinja2Templates(directory="templates")

###터미널 메시지는 정상인데, URL접속 시 무한로딩이 되는 경우, 포트가 여전히 가동중이라서 일어날 수 있습니다.
###접속 중 Ctrl+S 로 코드 저장 시 다시 되는 경우가 있다.


####################회원가입 코드#######################
@second_test.get("/register", response_class=HTMLResponse)
def show_register(request: Request):
   return templates.TemplateResponse("register.html",context={"request":request}) 



@second_test.post("/register")
def create_user(form_username: str=Form(...),form_password: str=Form(...),db: Session=Depends(get_db)):
  hashed_password=bcrypt.hashpw(form_password.encode('utf-8'),bcrypt.gensalt())
  db_user=Shoppers(
     user_name=form_username,
     password=hashed_password.decode('utf-8')
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return {"message" : "User created succesfully"}
############################################################


###################로그인 코드#################################
SECRET_KEY="secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

pwd_content=CryptContext(schemes=["bcrypt"],deprecated="auto")  #해시관련

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")  #토큰 URL...? 

def verify_password(plain_password: str, hashed_password: str)-> bool:  #비밀번호 검증 함수. CryptContext에는 검증 기능도 있구나...
   return pwd_content.verify(plain_password, hashed_password)   #평문과 해시 비밀번호를 비교

def get_user(db: Session, user_name: str):  #사용자 조회용
   return db.query(Shoppers).filter(Shoppers.user_name==user_name).first() #first는 데이터베이스와 비교하여 일치하는 첫 데이터를 반환
                                                                           #Shoppers의 user_name은 실제로 모델에 있는 속성

def authenticate_user(db: Session, auth_user_name:str, password: str):  #사용자 인증 함수
   user=get_user(db, auth_user_name)  #위의 사용자 조회용 코드 
   if not user or not verify_password(password, user.password): #get_user를 통해 user가 존재하는 지 가져옴, 동시에 비밀번호도 있는지 확인
      return False
   return user  #조건 만족 -> User의 이름을 그대로 반환

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):   #토큰 생성용 함수
   to_encode=data.copy()
   if expires_delta:
      expire=datetime.now(timezone.utc)+expires_delta
   else:
      expire=datetime.now(timezone.utc)+timedelta(minutes=15)
   to_encode.update({"exp":expire})
   encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)   #나중에 인증 시, 이 토큰은 같은 키와 알고리즘으로 decode됨
   return encoded_jwt


@second_test.get("/login")
def login_user(request: Request, response_class=HTMLResponse):
   return templates.TemplateResponse("login.html",context={"request": request})

@second_test.post("/login")
def login(request: Request, form_username: str=Form(...), form_password: str=Form(...), db: Session=Depends(get_db)):
   user=authenticate_user(db, form_username, form_password) #authenticate은 user를 반환. 그런데 이때 user안에는, 
                                                            #실제 데이터베이스의 특성이 들어가있다.(좀 특이함.) 
   if not user:   #만약 user가 아니라면
       raise HTTPException(  #접근 금지. 이 코드가 돌아가면, 밑의 남은 함수의 코드는 돌아가지 않는다. 
          status_code=status.HTTP_401_UNAUTHORIZED, 
          detail="Incorrect username or password",
          headers={"WWW-Authenticate":"Bearer"},
       )
     
   access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   access_token=create_access_token(  #토큰 생성 함수 내가 선언한 거. 
      data={"sub":user.user_name}, expires_delta=access_token_expires   #user 객체에는 실제 데이터베이스의 특성이 들어있음.
   )
   response=RedirectResponse(url="/welcome", status_code=status.HTTP_302_FOUND)  #유저일 경우, Redirect 객체 생성
   response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True) #Redirect 객체에 대한 쿠키 생성
   return response  #Redirect 객체 반환


@second_test.get("/welcome")
def welcome(request: Request):
   token = request.cookies.get("access_token")  #위의 set_cookie의 키 값(access_token)
   if token is None:  #애초에 정상적인 처리가 아니라면 토큰이 없다.
     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
   try:
      payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      user_name:str=payload.get("sub") #sub => user.username
      if user_name is None:  #느낌상 토큰이 없다면 여기서 될 리가 없다
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
   except JWTError:  #다른 이유의 토큰 에러인듯. try 관련 코드에서 예외적인 게 생길 시, 이런 코드가 돌아간다. 
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")    
   return templates.TemplateResponse("welcome.html", {"request":request, "user_name":user_name})


@second_test.get("/", response_class=HTMLResponse)    #get안에 htmlresponse 매개변수를 넣는 방법도 있음
def test2(request:Request, db:Session=Depends(get_db)): #db:Session = Depends(get_db)) -> 이게 한번에 적용할 수 있는 좋은 방법. 
    #models=Pistol_Armory()  #이런 복잡한 것들을 db.query문으로 간단하게 구현할 수도 있는 듯
                            #지금처럼 하나하나 다 명시하냐, 아니면 한번에 다 가져오냐의 문제
    #return templates.TemplateResponse("show_info.html",{
        #"request":request,
        #"Name":models.pistol_name,
        #"Type":models.pistol_type,
        #"ID":models.id
    #}, context={'request':request})
    laptop_info=db.query(Laptop_Models).all()
    return templates.TemplateResponse('show_info.html', {"request": request, "laptops" : laptop_info})

#get 메소드와 post 메소드를 명확히 하지 않으면 detail : method not allowed 오류가 난다!


@second_test.get('/upload',response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse("upload.html",context={"request":request})


@second_test.post("/upload", response_class=RedirectResponse)
def upload(form_laptop_cpu:str = Form(...),
            form_laptop_gpu:str=Form(...), 
            form_laptop_display_inch : float = Form(...),
            form_laptop_price : int = Form(...), 
            db: Session=Depends(get_db)):
 pd_laptop=Laptop_pydantic(
    laptop_cpu=form_laptop_cpu, 
    laptop_gpu=form_laptop_gpu, 
    laptop_display_inch=form_laptop_display_inch,
    laptop_price=form_laptop_price)
  
 db_laptop = Laptop_Models(
    laptop_cpu=pd_laptop.laptop_cpu, 
    laptop_gpu=pd_laptop.laptop_gpu,
    laptop_display_inch=pd_laptop.laptop_display_inch,
    laptop_price=pd_laptop.laptop_price) #모델과 pydantic 사이의 매핑
 
 db.add(db_laptop)
 db.commit()
 db.refresh(db_laptop)
 return RedirectResponse(url="/", status_code=303)

 


