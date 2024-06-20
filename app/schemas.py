from pydantic import BaseModel, HttpUrl


class URL(BaseModel):
    original_url: HttpUrl

    class Config:
        orm_mode = True


class URLStats(URL):
    stats: int
