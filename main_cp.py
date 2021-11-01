import json

from datetime import datetime
from typing import Optional, List

from pytz import timezone
from pydantic import BaseModel
from fastapi import FastAPI, status, Depends, HTTPException, Query, Body, Request, Cookie, WebSocket
from sqlalchemy.orm import Session

from starlette.middleware.cors import CORSMiddleware

import schemas
import models
from database import get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


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

# @app.get('/channel/')
# def show(
# date:str = Query(
# ..., 
# min_length=16, 
# max_length=16, 
# regex="[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}",
# title='연-월-일 시:분',
# description='연-월-일 시:분',
#     ),
# server_id:str = Query(...),
# db:Session = Depends(get_db)
# ):
#     date_time_obj = datetime. strptime(date, '%d-%m-%y %H:%M')
#     print('*'*100)
#     print(date)
#     print('*'*100)
#     print(date_time_obj)
#     print(type(date_time_obj))
#     # blog = db.query(models.Channel).filter(models.Channel.date == date).first()
#     # if not blog:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
#     # return blog
#     return f'{date} {server_id}'

# @app.post('/channel/fake-data')
# def create(fake_number:int, db: Session = Depends(get_db)):
#     from datetime import datetime, timedelta
#     import pytz
#     import random
#     seoul_time = pytz.timezone('Asia/Seoul')
#     current_time = datetime.now(seoul_time)
#     db.bulk_save_objects([
#         models.Channel(
#         date=current_time+timedelta(minutes=-number),
#         server_id=random.choice(['193', '192']),
#         ch_total=20,
#         ch_grpc=random.choice(list(range(1,11))),
#         ch_rest=random.choice(list(range(1,11))),
#         ) for number in range(1, fake_number+1)
#     ],return_defaults=True)
#     db.commit()
    
#     return db.query(models.Channel).all()

# @app.get('')
# def hello_world():
#     return 'hello world'


from fastapi import WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from collections import defaultdict

class Notifier:
    """
        Manages chat room sessions and members along with message routing
    """

    def __init__(self):
        self.connections: dict = defaultdict(dict)
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            msg = message["message"]
            room_name = message["room_name"]
            await self._notify(msg, room_name)

    def get_members(self, room_name):
        try:
            return self.connections[room_name]
        except Exception:
            return None

    async def push(self, msg: str, room_name: str = None):
        message_body = {"message": msg, "room_name": room_name}
        await self.generator.asend(message_body)

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        if self.connections[room_name] == {} or len(self.connections[room_name]) == 0:
            self.connections[room_name] = []
        self.connections[room_name].append(websocket)
        print(f"CONNECTIONS : {self.connections[room_name]}")

    def remove(self, websocket: WebSocket, room_name: str):
        self.connections[room_name].remove(websocket)
        print(
            f"CONNECTION REMOVED\nREMAINING CONNECTIONS : {self.connections[room_name]}"
        )

    async def _notify(self, message: str, room_name: str):
        living_connections = []
        while len(self.connections[room_name]) > 0:

            websocket = self.connections[room_name].pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections[room_name] = living_connections


notifier = Notifier()

templates = Jinja2Templates(directory='templates')


@app.get("/{room_name}/{user_name}")
async def get(request:Request, room_name, user_name):
    return templates.TemplateResponse(
        "chat_room.html",
        {"request": request, "room_name": room_name, "user_name": user_name},
    )


@app.websocket("/ws/{room_name}")
async def websocket_endpoint(
    websocket: WebSocket, room_name, background_tasks: BackgroundTasks
):

    await notifier.connect(websocket, room_name)

    try:
        while True:
            data = await websocket.receive_text()
            d = json.loads(data)
            d['room_name'] = room_name

            room_members = (notifier.get_members(room_name) if notifier.get_member(room_name) is not None else [])

            if websocket not in room_members: 
                print('SENDER NOT IN ROOM MEMBERS: RECONNECTING')
                await notifier.connect(websocket, room_name)
            
            await notifier._notify(f'{data}', room_name)
    except WebSocketDisconnect:
        notifier.remove(websocket, room_name)


# async def get_cookie_or_token(
#     websocket: WebSocket,
#     session: Optional[str] = Cookie(None),
#     token: Optional[str] = Query(None),
# ):
#     if session is None and token is None:
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#     return session or token


# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str, manager=Depends(ConnectionManager)):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")