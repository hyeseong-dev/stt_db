import asyncio 

import time
import pytz
import random
from datetime import datetime, timedelta

from fastapi_utils.tasks import repeat_every
from fastapi import Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

import models
from database import get_db

NUMBER = 0 
@repeat_every(seconds=3)
def data_generator(db: Session):
    global NUMBER
    seoul_time = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(seoul_time)
    number = 0
    print(number)
    channel = models.Channel(
        date=current_time+timedelta(minutes=-NUMBER),
        server_id=random.choice(['193', '192']),
        ch_total=20,
        ch_grpc=random.choice(list(range(1,11))),
        ch_rest=random.choice(list(range(1,11))),
        )
    db.add(channel)
    db.commit()
    NUMBER+=1



async def data_generator_task(db: Session = Depends(get_db), background_task: BackgroundTasks = BackgroundTasks):
    background_task.add_task(data_generator(db))
    return None