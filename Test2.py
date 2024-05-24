from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models.Pistol_Models import Pistol_Armory 
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

second_test=FastAPI()

templates=Jinja2Templates(directory="templates")

@second_test.get("/", response_class=HTMLResponse)
def test2(request:Request):
    models=Pistol_Armory()
    return templates.TemplateResponse("index.html",{
        "request":request,
        "Name":models.pistol_name,
        "Type":models.pistol_type,
        "ID":models.id
    })