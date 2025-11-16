from celery import Celery
from celery.signals import worker_process_init
from src.infrastructure.config.env_config_service import EnvConfigService
from src.infrastructure.database.mappers import start_mappers

config_service = EnvConfigService()
redis_url = config_service.get_redis_url()

celery_app = Celery(
    'task_manager',
    broker=redis_url,
    backend=redis_url,
    include=['src.infrastructure.celery.handlers']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@worker_process_init.connect
def init_worker_process(sender=None, **kwargs):
    start_mappers()
