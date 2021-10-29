from typing import Optional
from fastapi import FastAPI, status, Depends, HTTPException
from pydantic import BaseModel
from database import get_db

# from sqlalchemy import Session


app = FastAPI()

# @app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def destory(id, db: Session=Depends(get_db)):
#     blog = db.query(models.Channel).filter


# @app.get('/blog')
# def all(db:Session = Depends(get_db)):
#     blog = db.query(models.Channel).all()
#     return blog


# @app.post('/blog')
# def create(request: schemas.Channel, db: Session = Depends(get_db)):
#     new_blog = models.Channel(title=request.title, body=request.body, user_id=request.creator)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

# @app.post('/user')
# def create(request:schemas.Channel, db: Session = Depends(get_db)):
#     new_user = models.Channel(name=request.name, email=request.email, password=request.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get('/blog/{id}')
# def show(id:int, db:Session = Depends(get_db)):
#     blog = db.query(models.Channel).filter(models.Channel.id == id).first()
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
#     return blog

  
@app.get('')
def hello_world():
    return 'hello world'

