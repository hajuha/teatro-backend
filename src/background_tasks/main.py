from core.schedulers.main import BackgroundTaskManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from background_tasks.similar_movie_from_movie import main as similar_movie_from_movie
from background_tasks.similar_movie_from_user import main as similar_movie_from_user

def init_background_tasks():
    new_background_task_scheduler = BackgroundTaskManager(AsyncIOScheduler())
    
    new_background_task_scheduler.remove_all_jobs()

    new_background_task_scheduler.add_job(
        similar_movie_from_user,
        id="similar_movie_from_user",
        # trigger="interval",
        # seconds=5*60, 
        # max_instances=1
    )
    
    new_background_task_scheduler.add_job(
        similar_movie_from_movie,
        id="similar_movie_from_movie",
        # trigger="interval",
        # seconds=5*60, 
        # max_instances=1
    )