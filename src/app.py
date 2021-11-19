from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response
import uvicorn
from src.apis.user import router as UserRouter
from src.apis.movie import router as MovieRouter

app = FastAPI()

app.include_router(UserRouter)
app.include_router(MovieRouter)