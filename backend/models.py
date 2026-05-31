from sqlmodel import SQLModel, Field
from enum import IntEnum
from typing import Optional
from datetime import datetime, timezone
from pydantic import field_serializer, field_validator

def utcnow():
  return datetime.now(timezone.utc)

class ServiceStatus(IntEnum):
  pending = 0
  healthy = 1
  degraded = 2
  down = 3

class Service(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str
  description: Optional[str] = None
  url: str
  status: int = Field(default=ServiceStatus.pending)
  response_time: Optional[float] = None
  last_checked_at: Optional[datetime] = None
  created_at: datetime = Field(default_factory=utcnow)
  updated_at: datetime = Field(default_factory=utcnow)

class ServiceCreate(SQLModel):
  name: str
  description: Optional[str] = None
  url: str
  status: ServiceStatus = ServiceStatus.pending

  @field_validator("status", mode="before")
  @classmethod
  def _accept_status_name(cls, v):
    if isinstance(v, str):
      return ServiceStatus[v]
    return v

class ServiceRead(SQLModel):
  id: int
  name: str
  description: Optional[str] = None
  url: str
  status: ServiceStatus
  response_time: Optional[float] = None
  last_checked_at: Optional[datetime] = None
  created_at: datetime
  updated_at: datetime

  @field_serializer("status")
  def _serialize_status(self, v: ServiceStatus) -> str:
    return v.name

class ServiceUpdate(SQLModel):
  name: Optional[str] = None
  description: Optional[str] = None
  url: Optional[str] = None
  status: Optional[ServiceStatus] = None
  @field_validator("status", mode="before")
  @classmethod
  def _accept_status_name(cls, v):
    if isinstance(v, str):
      return ServiceStatus[v]
    return v
