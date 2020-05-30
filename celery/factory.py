from flask import Flask
from celery import Celery


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    return app


def create_celery(app=None):
    app = app or create_app()
    celery = Celery(__name__)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class _ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = _ContextTask
    return celery
