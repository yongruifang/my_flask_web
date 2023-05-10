from celery import Celery
import time

def atask(a,b):
    time.sleep(5000)  
    return {"status":"SUCCESS"}

def make_celery(app):
    celery = Celery(app.import_name,
                    backend='redis://localhost:6379/1',
                    broker='redis://localhost:6379/2')
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self,*args,**kwargs):
            with app.app_context():
                return TaskBase.__call__(self,*args,**kwargs)
            
    celery.Task = ContextTask
    app.celery = celery

    # 添加任务

    celery.task(name='atask')(atask)

    return celery
