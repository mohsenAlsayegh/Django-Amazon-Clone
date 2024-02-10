from celery import shared_task
import time

@shared_task
def excute_code():
    for x in range(10):
        print(x)
        time.sleep(1)