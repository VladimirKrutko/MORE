from fastapi import FastAPI
from starlette.requests import Request
import uvicorn
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from MORE_FAST_API.model.more_db import More_DB_commnad


app = FastAPI()

data_db = More_DB_commnad(dbname='more', user='postgres', password='1458', host='localhost') 
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}
    )
if __name__ == "__main__":
    uvicorn.run('main:app',reload=True)