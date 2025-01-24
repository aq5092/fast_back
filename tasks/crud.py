from sqlalchemy.orm import Session
from . import schemas, models

################################################
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
    
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()
 

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db:Session,task:schemas.TaskBase):
    db_task = models.Task(task_name=task.task_name)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task: schemas.TaskCreate, task_id: int):
    # Update the user
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_task.task_name = task.task_name
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    # Delete the user
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db.delete(db_task)
    db.commit()
    return db_task

