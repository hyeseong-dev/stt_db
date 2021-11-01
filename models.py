from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from sqlalchemy.orm import relationship


class Channel(Base):
    __tablename__ = 'channel'
    date = Column(DateTime, primary_key=True, index=True)
    server_id = Column(String, primary_key=True, index=True)
    ch_total = Column(Integer)
    ch_grpc = Column(Integer)
    ch_rest = Column(Integer)
    


