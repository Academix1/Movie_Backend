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
    return response.data;
  } catch (error) {
    console.error("Error creating movie:", error);
    throw error;
  }
};

// Update an existing movie
export const updateMovie = async (movieId, movieData) => {
  try {
    const response = await axios.put(`${BASE_URL}/${movieId}`, movieData);
    return response.data;
  } catch (error) {
    console.error(`Error updating movie ${movieId}:`, error);
    throw error;
  }
};

// Delete a movie
export const deleteMovie = async (movieId) => {
  try {
    const response = await axios.delete(`${BASE_URL}/${movieId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting movie ${movieId}:`, error);
    throw error;
  }
};
```
### `Movielist.js`

```js
import React, { useEffect, useState } from "react";
import {
  getMovies,
  getMovieById,
  createMovie,
  updateMovie,
  deleteMovie,
} from "../api/axiosMoviesApi";

const MoviesList = () => {
  const [movies, setMovies] = useState([]);
  const [newMovie, setNewMovie] = useState({
    title: "",
    director: "",
    release_year: "",
    poster_url: "",
    price: "",
  });
  const [editingMovieId, setEditingMovieId] = useState(null);
  const [editingMovieData, setEditingMovieData] = useState(null);

  useEffect(() => {
    fetchMovies();
  }, []);

  const fetchMovies = async () => {
    try {
      const data = await getMovies();
      setMovies(data);
    } catch (error) {
      console.error("Error fetching movies:", error);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await createMovie(newMovie);
      setNewMovie({ title: "", director: "", release_year: "", poster_url: "", price: "" });
      fetchMovies();
    } catch (error) {
      console.error("Error creating movie:", error);
    }
  };

  const handleEdit = async (movieId) => {
    try {
      const movieData = await getMovieById(movieId);
      setEditingMovieId(movieId);
      setEditingMovieData(movieData);
    } catch (error) {
      console.error("Error fetching movie for edit:", error);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    if (!editingMovieId) return;

    try {
      await updateMovie(editingMovieId, editingMovieData);
      setEditingMovieId(null);
      setEditingMovieData(null);
      fetchMovies();
    } catch (error) {
      console.error("Error updating movie:", error);
    }
  };

  const handleDelete = async (movieId) => {
    try {
      await deleteMovie(movieId);
      setMovies(movies.filter((movie) => movie.id !== movieId));
    } catch (error) {
      console.error("Error deleting movie:", error);
    }
  };

  return (
    <div>
      <h2>Movies List</h2>
      <ul>
        {movies.map((movie) => (
          <li key={movie.id}>
            {editingMovieId === movie.id && editingMovieData ? (
              // Show input fields if movie is being edited
              <div>
                <input
                  type="text"
                  value={editingMovieData.title}
                  onChange={(e) =>
                    setEditingMovieData({ ...editingMovieData, title: e.target.value })
                  }
                />
                <input
                  type="text"
                  value={editingMovieData.director}
                  onChange={(e) =>
                    setEditingMovieData({ ...editingMovieData, director: e.target.value })
                  }
                />
                <input
                  type="number"
                  value={editingMovieData.release_year}
                  onChange={(e) =>
                    setEditingMovieData({ ...editingMovieData, release_year: e.target.value })
                  }
                />
                <input
                  type="text"
                  value={editingMovieData.poster_url}
                  onChange={(e) =>
                    setEditingMovieData({ ...editingMovieData, poster_url: e.target.value })
                  }
                />
                <input
                  type="number"
                  value={editingMovieData.price}
                  onChange={(e) =>
                    setEditingMovieData({ ...editingMovieData, price: e.target.value })
                  }
                />
                <button onClick={handleUpdate}>Update</button>
                <button onClick={() => setEditingMovieId(null)}>Cancel</button>
              </div>
            ) : (
              // Show normal text if not being edited
              <div>
                <h3>{movie.title}</h3>
                <p>Director: {movie.director}</p>
                <p>Poster URL: {movie.poster_url}</p>
                <p>Year: {movie.release_year}</p>
                <p>Price: ${movie.price}</p>
                <button onClick={() => handleEdit(movie.id)}>Edit</button>
                <button onClick={() => handleDelete(movie.id)}>Delete</button>
              </div>
            )}
          </li>
        ))}
      </ul>

      {/* Form to create a new movie */}
      <h2>Add New Movie</h2>
      <form onSubmit={handleCreate}>
        <input
          type="text"
          placeholder="Title"
          value={newMovie.title}
          onChange={(e) => setNewMovie({ ...newMovie, title: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Director"
          value={newMovie.director}
          onChange={(e) => setNewMovie({ ...newMovie, director: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Release Year"
          value={newMovie.release_year}
          onChange={(e) => setNewMovie({ ...newMovie, release_year: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Poster URL"
          value={newMovie.poster_url}
          onChange={(e) => setNewMovie({ ...newMovie, poster_url: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Price"
          value={newMovie.price}
          onChange={(e) => setNewMovie({ ...newMovie, price: e.target.value })}
          required
        />
        <button type="submit">Create</button>
      </form>
    </div>
  );
};

export default MoviesList;
```
