from fastapi import FastAPI
from fastapi import Form
from starlette.requests import Request
import uvicorn
from pydantic import BaseModel
# from fastapi.responses import HTMLResponse
# from starlette.responses import FileResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sys
sys.path.append('/home/uladzimir/MORE/MORE_FAST_API/model')
from more_db import More_DB_commnad

app = FastAPI()

data_db = More_DB_commnad('more','postgres', '1458', 'localhost') 

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

@app.get("/country")
async def select_country(request:Request):
    country = data_db.select_country()
    return templates.TemplateResponse("table.html", {"request": request, "country":country})

@app.get("/sapliers")
async def select_suplier(request:Request):
    sup = data_db.select_suplier()
    return templates.TemplateResponse("saplier.html", {"request": request, "suplier":sup})

@app.get("/delivery")
async def select_delivery(request:Request):
    delivery = data_db.select_delivery()
    return templates.TemplateResponse("delivery.html", {"request": request, "delivery":delivery})

@app.get("/warehouse")
async def select_warehouse(request:Request):
    warehouse=data_db.select_warehouse()
    print(warehouse)
    return templates.TemplateResponse("warehouse.html", {"request": request, "warehouse":warehouse})

@app.get('/menu_maker')
async def menu_maker(request:Request):
    return templates.TemplateResponse('menu_maker.html',  {"request": request})

@app.post("/input_sales")
async def create_upload_files(request:Request, product: str = Form(...), quantity: int = Form(...)):
    data_db.insert_sales(product, quantity)
    data_db.send_email('krutkovova24@gmail.com', product)
    return templates.TemplateResponse('menu_maker.html',  {"request": request})


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}
    )

if __name__ == "__main__":
    uvicorn.run('main:app',reload=True)
    