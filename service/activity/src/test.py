from fastapi import FastAPI
from fastapi_crudrouter import MemoryCRUDRouter
from pydantic import BaseModel


class Potato(BaseModel):
    id: int
    color: str
    mass: float


app = FastAPI()
router = MemoryCRUDRouter(schema=Potato)
app.include_router(router)
