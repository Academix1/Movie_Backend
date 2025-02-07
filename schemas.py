# schemas.py
from pydantic import BaseModel

# Base schema for common movie fields
class MovieBase(BaseModel):
    title: str
    director: str
    release_year: int
    poster_url: str
    price: float

class Movie(MovieBase):
    id: int 
