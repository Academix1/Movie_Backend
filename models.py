# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Movie(Base):
    __tablename__ = "movies"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    director = Column(String)
    release_year = Column(Integer)
    poster_url = Column(String)  # URL to the movie poster
    price = Column(Float)

