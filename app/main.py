from fastapi import FastAPI
from .routes.user_route import router as UserRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/", tags=["Root"])
def read_root():
    return {"Message": "Welcome to DermaCam Backend End !!!"}
