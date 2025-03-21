from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from .auth import createAccessToken, verifyPassword
from .gRPCHandler import getAccountByEmail
from .api.account import account
from .api.courses import course, courseProgress
from .api.assessment import assessment
from .api.job import job
from .api.certificate import certificate

from .models import Token
from datetime import timedelta
import os 

TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

currentPath = os.path.dirname(os.path.abspath(__file__))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to all just for ease of development. In actual use, it should be limited to specific ones
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HTML_FILE_PATH = currentPath + "/public/index.html"

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await getAccountByEmail(form_data.username)
    if not user or not verifyPassword(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    accessTokenExpiry = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    accessToken = createAccessToken(data={"sub": user.userId}, expireDelta=accessTokenExpiry)
    return {"access_token": accessToken, "token_type": "bearer"}

app.include_router(account)
app.include_router(course)
app.include_router(assessment)
app.include_router(job)
app.include_router(certificate)
app.include_router(courseProgress)
app.mount("/", StaticFiles(directory=currentPath + "/public", html = True), name="static")

def read_404_html():
    with open(HTML_FILE_PATH, "r") as file:
        return file.read()

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    html_content = read_404_html()
    return HTMLResponse(content=html_content, status_code=404)
