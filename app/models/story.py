from pydantic import BaseModel


class Story(BaseModel):
    title: str
    comments: int
    points: int
    rank: int