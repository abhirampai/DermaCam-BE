from fastapi import FastAPI
from .routes.user_route import router as UserRouter

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/",tags=["Root"])
def read_root():
    return {"Message":"Welcome to DermaCam Backend End !!!"}