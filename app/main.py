from fastapi import FastAPI, File, UploadFile
from .routes.user_route import router as UserRouter
from fastapi.middleware.cors import CORSMiddleware
from .db import cloudinary

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


@app.get("/")
def read_root():
    return {"Message": "Welcome to DermaCam Backend End !!!"}


@app.post("/uploadImage", response_description="Return Image Url")
async def uploadImage(image: UploadFile = File(...)):
    result = cloudinary.uploader.upload(image.file)
    return {
        'data': result['url']
    }
