import uvicorn
from fastapi import FastAPI
from controller.routers import jarvis_operacoes, running
from shared.database import Base, engine
from shared.database import *

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(jarvis_operacoes.router)
app.include_router(running.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
# http://localhost:8000/
# http://localhost:8000/docs
