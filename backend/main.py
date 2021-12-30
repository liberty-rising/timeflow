from fastapi import *
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import OperationalError
from backend.models.user import User
from backend.models.timelog import TimeLog
from backend.models.epic import Epic
from backend.models.client import Client
from backend.utils import engine, create_db
import datetime
from backend.api import user, timelog, forecast, epic, client, rate

app = FastAPI()
session = Session(engine)
app.include_router(timelog.router)
app.include_router(forecast.router)
app.include_router(user.router)
app.include_router(epic.router)
app.include_router(client.router)
app.include_router(rate.router)


@app.on_event("startup")
def on_startup():
    try:
        statement = select(TimeLog)
        results = session.exec(statement)
    except OperationalError:
        create_db()
