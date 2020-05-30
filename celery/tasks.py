from factory import create_celery

queue = create_celery()


@queue.task
def add(x, y):
    import time
    time.sleep(1)
    return x + y
