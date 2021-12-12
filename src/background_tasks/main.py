from core.schedulers.main import BackgroundTaskManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from background_tasks.rating_data_to_data import main as rating_data_to_data 
def init_background_tasks():
    new_background_task_scheduler = BackgroundTaskManager(AsyncIOScheduler())
    
    new_background_task_scheduler.remove_all_jobs()

    # new_background_task_scheduler.add_job(
    #     rating_data_to_data,
    #     id="rating_data_to_data",
    #     # trigger="interval",
    #     # seconds=5, 
    #     # max_instances=1
    # )