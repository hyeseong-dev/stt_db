from datetime import datetime
from pydantic import BaseModel


class Channel(BaseModel):
    date: str
    server_id: str
    ch_total : int
    ch_grpc : int 
    ch_rest : int 
    
