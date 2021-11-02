from celery import shared_task

@shared_task
def divide(x,y):
    return x /y