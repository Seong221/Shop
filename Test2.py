from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from models.Shop_models import Laptop_Models, Laptop_pydantic
from fastapi.templating import Jinja2Templates
from database.db_link import get_db, given_table, engine
from sqlalchemy.orm import Session


###API 호출, 프론트엔드에서 버튼 입력 -> DB에 저장, 만든 사이트를 aws에서 서비스하고 그 IP로 접속이 되는 지 확인하는 게 중요###


second_test=FastAPI()
#session=Session() 이 부분 때문에 오류가 난 듯합니다. session은 의존성 주입을 사용해야 된다고 하더군요. 
#이렇게 session 객체를 만들고 함수 안에 db대신 썼더니 UnBound 오류가 난 듯 합니다. 

given_table.metadata.create_all(bind=engine) #데이터베이스에 테이블 생성이라는 의미

templates=Jinja2Templates(directory="templates")

###터미널 메시지는 정상인데, URL접속 시 무한로딩이 되는 경우, 포트가 여전히 가동중이라서 일어날 수 있습니다.
###접속 중 Ctrl+S 로 코드 저장 시 다시 되는 경우가 있다.


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



