from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi.staticfiles import StaticFiles
import db_models
from db_session import engine
from sqlalchemy.orm import Session
from db_handler import DBHandler, get_db
from gpio_handler import GPIOHandler
import sys
import os

parent_dir_path = os.path.dirname(os.path.realpath(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory=parent_dir_path+"/static"), name="static")
templates = Jinja2Templates(directory=parent_dir_path+"/templates")
db_models.Base.metadata.create_all(bind=engine)
db_handler = DBHandler()
print(parent_dir_path)


@app.get("/")
@app.get("/home")
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })


@app.get("/get-logging-data")
async def get_logging_data(request: Request, db: Session = Depends(get_db)):
    try:
        logging_data = db_handler.get_logging_list(db)
        return logging_data
    except:
        raise HTTPException(status_code=500, detail="\
        Fetching data not possible at the moment. Try again later.")


@app.post("/do-routine")
async def do_routine(response: Response):
    handler = GPIOHandler()
    handler.do_routine()
    del handler
    return {
        "response": response,
    }


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
    else:
        ip_address = '127.0.0.1'
    uvicorn.run(app, host=ip_address, port=8080)
