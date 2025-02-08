### `api.js`

```js
import axios from "axios";

const BASE_URL = "http://localhost:8000/movies"; // FastAPI backend URL

// Fetch all movies
export const getMovies = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching movies:", error);
    throw error;
  }
};

// Fetch a single movie by ID
export const getMovieById = async (movieId) => {
  try {
    const response = await axios.get(`${BASE_URL}?movie_id=${movieId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching movie ${movieId}:`, error);
    throw error;
  }
};

// Create a new movie
export const createMovie = async (movieData) => {
  try {
    const response = await axios.post(`${BASE_URL}/create`, movieData);
    console.log("Created movie:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error creating movie:", error);
    throw error;
  }
};

// Update an existing movie
export const updateMovie = async (movieId, movieData) => {
  try {
    const response = await axios.put(`${BASE_URL}?id=${movieId}`, movieData);
    console.log("Updated movie:", response.data);
    return response.data;
  } catch (error) {
    console.error(`Error updating movie ${movieId}:`, error);
    throw error;
  }
};

// Delete a movie
export const deleteMovie = async (id) => {
    console.log("Deleting movie with ID:", id); // Debugging line
    if (!id) {
      console.error("Error: movie_id is undefined");
      return;
    }
  
    try {
      const response = await axios.delete(`${BASE_URL}?id=${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting movie ${id}:`, error);
      throw error;
    }
  };
  

```
### `Movielist.js`

```js
import React, { useEffect, useState } from "react";
import { getMovies, createMovie, deleteMovie, updateMovie } from "../api/axiosMoviesApi"; // Import API functions

const MoviesList = () => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingMovieId, setEditingMovieId] = useState(null); // Track editing mode
  const [movieForm, setMovieForm] = useState({
    title: "",
    director: "",
    release_year: "",
    price: "",
    poster_url: "",
  });

  // Fetch all movies on component mount
  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const data = await getMovies();
        setMovies(data);
      } catch (error) {
        console.error("Error fetching movies:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchMovies();
  }, []);

  // Handle movie deletion
  const handleDelete = async (movieId) => {
    if (!movieId) {
      console.error("Error: movieId is undefined!");
      return;
    }
    try {
      await deleteMovie(movieId);
      setMovies((prevMovies) => prevMovies.filter((movie) => movie.id !== movieId));
    } catch (error) {
      console.error("Error deleting movie:", error);
    }
  };

  // Handle adding/updating a movie
  const handleSaveMovie = async () => {
    if (!movieForm.title || !movieForm.director) {
      alert("Title and Director are required!");
      return;
    }

    try {
      if (editingMovieId) {
        // Update movie if in edit mode
        const updatedMovie = await updateMovie(editingMovieId, movieForm);
        setMovies((prevMovies) =>
          prevMovies.map((movie) => (movie.id === editingMovieId ? updatedMovie : movie))
        );
        setEditingMovieId(null); // Exit edit mode
      } else {
        // Add a new movie
        const addedMovie = await createMovie(movieForm);
        setMovies((prevMovies) => [...prevMovies, addedMovie]);
      }

      // Reset form fields after adding/updating
      setMovieForm({ title: "", director: "", release_year: "", price: "", poster_url: "" });
    } catch (error) {
      console.error("Error saving movie:", error);
    }
  };

  // Handle movie edit click
  const handleEditMovie = (movie) => {
    setEditingMovieId(movie.id);
    setMovieForm({
      title: movie.title,
      director: movie.director,
      release_year: movie.release_year,
      price: movie.price,
      poster_url: movie.poster_url,
    });
  };

  if (loading) return <p>Loading movies...</p>;

  return (
    <div>
      <h1>Movie List</h1>
      {/* Movie Input Form */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Title"
          value={movieForm.title}
          onChange={(e) => setMovieForm({ ...movieForm, title: e.target.value })}
        />
        <input
          type="text"
          placeholder="Director"
          value={movieForm.director}
          onChange={(e) => setMovieForm({ ...movieForm, director: e.target.value })}
        />
        <input
          type="number"
          placeholder="Release Year"
          value={movieForm.release_year}
          onChange={(e) => setMovieForm({ ...movieForm, release_year: e.target.value })}
        />
        <input
          type="number"
          placeholder="Price"
          value={movieForm.price}
          onChange={(e) => setMovieForm({ ...movieForm, price: e.target.value })}
        />
        <input
          type="text"
          placeholder="Poster URL"
          value={movieForm.poster_url}
          onChange={(e) => setMovieForm({ ...movieForm, poster_url: e.target.value })}
        />
        <button onClick={handleSaveMovie}>
          {editingMovieId ? "Save Changes" : "Add Movie"}
        </button>
      </div>

      {/* Movies List */}
      <div>
        {movies.length > 0 ? (
          movies.map((movie) => (
            <div
              key={movie.id || Math.random()} // Ensure unique key
              style={{
                border: "1px solid #ccc",
                padding: "10px",
                marginBottom: "10px",
              }}
            >
              <h3>{movie.title}</h3>
              <p>Director: {movie.director}</p>
              <p>Release Year: {movie.release_year}</p>
              <img src={movie.poster_url} alt={movie.title} style={{ maxWidth: "100px", maxHeight: "150px" }} />
              <p>Price: ${movie.price}</p>
              <button
                onClick={() => handleDelete(movie.id)}
                style={{ background: "red", color: "white", marginRight: "10px" }}
              >
                Delete
              </button>
              <button
                onClick={() => handleEditMovie(movie)}
                style={{ background: "blue", color: "white" }}
              >
                Update
              </button>
            </div>
          ))
        ) : (
          <p>No movies found.</p>
        )}
      </div>
    </div>
  );
};

export default MoviesList;
```
