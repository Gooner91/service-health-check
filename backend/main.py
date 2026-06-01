from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session, create_db
from models import Service, ServiceRead, ServiceCreate, ServiceUpdate, utcnow
app = FastAPI()

@app.on_event("startup")
def on_startup():
  create_db()

@app.get("/services", response_model=list[ServiceRead])
def list_services(session: Session = Depends(get_session)):
  return session.exec(select(Service)).all()

@app.post("/services", response_model=ServiceRead)
def create_service(payload: ServiceCreate, session: Session = Depends(get_session)):
  service = Service.model_validate(payload)
  session.add(service)
  session.commit()
  session.refresh(service)
  return service

@app.patch("/services/{id}", response_model=ServiceRead)
def update_service(id: int, payload: ServiceUpdate, session: Session = Depends(get_session)):
  service = session.get(Service, id)
  if service is None:
    raise HTTPException(status_code=404, detail="Service not found")
  data = payload.model_dump(exclude_unset=True)
  service.sqlmodel_update(data)
  service.updated_at = utcnow()
  session.commit()
  session.refresh(service)
  return service

@app.delete("/services/{id}", status_code=204)
def delete_service(id: int, session: Session = Depends(get_session)):
  service = session.get(Service,id)
  if service is None:
    raise HTTPException(status_code=404, detail="Service not found")
  session.delete(service)
  session.commit()



