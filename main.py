from fastapi import FastAPI, HTTPException, Depends, status, HTTPException
from sqlalchemy.orm import Session
from users import crud, schemas, models
from database import SessionLocal, engine
from typing import List
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://aq5092-otnfront-c607.twc1.net"
]
app.add_middleware (
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/userc/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)

@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@app.put('/useru/{user_id}', response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud.update_user(db=db, user=user, user_id=user_id)

@app.delete('/userd/{user_id}', response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud.delete_user(db=db, user_id=user_id)


#@app.post('/users/{user_id}/posts/', response_model=schemas.Post)
#def create_post_for_user(user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
#    return crud.create_post(db=db, post=post, user_id=user_id)

#@app.get('/posts/', response_model=List[schemas.Post])
#def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    posts = crud.get_posts(db, skip=skip, limit=limit)
#    return posts

