from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

from django.db import connection
import celery

class FaultTolerantTask(celery.Task):
    """ Implements after return hook to close the invalid connection.
    This way, django is forced to serve a new connection for the next
    task.
    """
    abstract = True

    def after_return(self, *args, **kwargs):
        connection.close()

@celery.task(base=FaultTolerantTask)
def my_task():
    # my database dependent code here

@app.task
def add(x, y):
    return x + y