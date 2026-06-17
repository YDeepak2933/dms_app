from pydantic import BaseModel
from typing import List, Optional

# -------- Data Element --------

class DataElementCreate(BaseModel):
    name: str
    data_type: str
    is_required: Optional[bool] = False
    is_unique: Optional[bool] = False

class DataElementResponse(BaseModel):
    id: str
    name: str
    data_type: str
    is_required: bool
    is_unique: bool

    class Config:
        orm_mode = True

# -------- Dataset --------

class DatasetCreate(BaseModel):
    name: str
    description: Optional[str]

class DatasetResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class DatasetWithElements(DatasetResponse):
    data_elements: List[DataElementResponse] = []
