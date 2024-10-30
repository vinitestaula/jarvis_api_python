from fastapi import APIRouter
from shared.database import *

router = APIRouter(prefix="")

@router.get("/")
def api_working():
    return "API está rodando."