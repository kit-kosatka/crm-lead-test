from pydantic import BaseModel, ConfigDict, Field


class LeadCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=1, max_length=30)
    source: str
    manager: str
    stage: str
    requested_tz: bool = False


class LeadRead(LeadCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
