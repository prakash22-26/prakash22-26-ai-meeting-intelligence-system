from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)

    transcript = Column(Text)

    summary = Column(Text)

    action_items = Column(Text)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )