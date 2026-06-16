from pydantic import BaseModel


class Article(BaseModel):
    title: str
    description: str
    source: str
    url: str

