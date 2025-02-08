from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from fastapi.staticfiles import StaticFiles
from database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS settings
origins = [
    "http://localhost:3000",  # Add the URL of your frontend app here
    # You can add more origins if needed
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Mount static files directory (optional)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/movies/create", status_code=status.HTTP_202_ACCEPTED)
def create(movie: schemas.MovieBase, db: Session = Depends(get_db)):
    new_movie = models.Movie(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return f"This {new_movie.title} has been saved successfully"

@app.get("/movies/", response_model=list[schemas.Movie])
def read(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).all()
    return movies

@app.get("/movies", response_model=schemas.Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie

@app.put("/movies", status_code=status.HTTP_202_ACCEPTED)
def update_movie(id: int, movie: dict, db: Session = Depends(get_db)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    if "poster_url" in movie:
        db_movie.poster_url = movie["poster_url"]
    if "title" in movie:
        db_movie.title = movie["title"]
    if "director" in movie:
        db_movie.director = movie["director"]
    if "release_year" in movie:
        db_movie.release_year = movie["release_year"]
    if "price" in movie:
        db_movie.price = movie["price"]
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.delete("/movies", status_code=status.HTTP_202_ACCEPTED)
def deletemovie(id: int, db: Session = Depends(get_db)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    return f"Movie {db_movie.title} has been deleted successfully"
