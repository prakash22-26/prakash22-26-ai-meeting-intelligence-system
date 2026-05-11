from pydantic import BaseModel

class MeetingCreate(BaseModel):
    transcript: str