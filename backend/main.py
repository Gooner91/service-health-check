from fastapi import FastAPI, Depends
from sqlmodel import Session, select

from database import get_session, create_db
from models import Service, ServiceCreate, ServiceUpdate
app = FastAPI()

@app.on_event("startup")
def on_startup():
  create_db()

@app.get("/services")
def list_services(session: Session = Depends(get_session)):
  return session.exec(select(Service)).all()

@app.post("/services")
def create_service(payload: ServiceCreate, session: Session = Depends(get_session)):
  service = Service.model_validate(payload)
  session.add(service)
  session.commit()
  session.refresh(service)
  return service
