from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response
import uvicorn
from apis.user import router as UserRouter
from apis.movie import router as MovieRouter
from apis.similar_movie import router as SimilarMovieRouter
from background_tasks.main import init_background_tasks
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from core.database.mongo import close_db, get_db_client


origins = [
    "http://localhost",
    "http://localhost:3000"
]

app = FastAPI(
    title=settings.PROJECT_NAME, docs_url="/docs", openapi_url="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def listener_server_start(*args, **kwargs):
    from core.schedulers.main import BackgroundTaskManager
    
    await get_db_client()
    init_background_tasks()
    BackgroundTaskManager.scheduler.start()
    print("server_start")

async def listener_server_stop(*args, **kwargs):
    from core.schedulers.main import BackgroundTaskManager
    await close_db()
    BackgroundTaskManager.scheduler.stop()
    print("server_stop")

app.add_event_handler("startup", listener_server_start)
app.add_event_handler("shutdown", listener_server_stop)

app.include_router(UserRouter,)
app.include_router(MovieRouter, prefix="/movie")
app.include_router(SimilarMovieRouter)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", reload=True, port=5001, debug=True, workers=3)