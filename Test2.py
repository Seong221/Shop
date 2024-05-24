from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from models.Pistol_Models import Pistol_Armory 
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from database.db_link import get_db
from sqlalchemy.orm import Session

###API 호출, 프론트엔드에서 버튼 입력 -> DB에 저장, 만든 사이트를 aws에서 서비스하고 그 IP로 접속이 되는 지 확인하는 게 중요###


second_test=FastAPI()
session=Session()

templates=Jinja2Templates(directory="templates")

###터미널 메시지는 정상인데, URL접속 시 무한로딩이 되는 경우, 포트가 여전히 가동중이라서 일어날 수 있습니다.
###접속 중 Ctrl+S 로 코드 저장 시 다시 되는 경우가 있다.


@second_test.get("/", response_class=HTMLResponse)    #get안에 htmlresponse 매개변수를 넣는 방법도 있음
def test2(request:Request): #db:Session = Depends(get_db)) -> 이게 한번에 적용할 수 있는 좋은 방법
    #models=Pistol_Armory()  #이런 복잡한 것들을 db.query문으로 간단하게 구현할 수도 있는 듯
                            #지금처럼 하나하나 다 명시하냐, 아니면 한번에 다 가져오냐의 문제
    #return templates.TemplateResponse("show_info.html",{
        #"request":request,
        #"Name":models.pistol_name,
        #"Type":models.pistol_type,
        #"ID":models.id
    #}, context={'request':request})
    pistol_info=session.query(Pistol_Armory).all()
    return templates.TemplateResponse('show_info.html', pistols=pistol_info)

#get 메소드와 post 메소드를 명확히 하지 않으면 detail : method not allowed 오류가 난다!


@second_test.get('/upload',response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse("upload.html",context={"request":request})


@second_test.post("/upload")
def upload(pistol_name:str=Form(...), pistol_type:str=Form(...), db: Session = Depends(get_db)):
    #보니까 등호 기준 pistol_name이 form에서 보낸 데이터고, 이걸 왼쪽 변수, 즉 진짜 데이터 모델의 변수가 받아야 되는 듯 하다!
    new_info=Pistol_Armory(pistol_name=pistol_name, pistol_type=pistol_type)
    db.add(new_info)
    db.commit()
    db.refresh(new_info)
    return RedirectResponse(url="/", status_code=303) #status code 303 = redirect to other url 
    

