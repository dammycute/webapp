from celery import Celery
from celery_config import broker_url

app = Celery('authApp', broker=broker_url)

if __name__ == '__main__':
    app.start