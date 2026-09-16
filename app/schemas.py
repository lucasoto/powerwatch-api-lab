from typing import Literal

from pydantic import BaseModel


class OutageCreate(BaseModel):
    region_id: int


class OutageUpdate(BaseModel):
    status: Literal["restabelecida"]


class OutageZoneCreate(BaseModel):
    zone: str
