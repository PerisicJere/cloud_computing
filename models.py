from pydantic import BaseModel

class getItemBody(BaseModel):
    id: int

class getItemResponse(BaseModel):
    id: int
    name: str
    desc: str
    damage: float