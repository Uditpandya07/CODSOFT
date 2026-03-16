# Task 4 — Movie Recommendation System (Python)

A movie recommendation system using collaborative filtering and cosine similarity on the MovieLens dataset.

## How it Works
- Uses **TF-IDF** on movie genres to build a feature matrix
- Computes **Cosine Similarity** between all movies
- Search by title → get similar movies with match percentage
- Browse by genre → get top rated movies in that genre

## Setup

```bash
pip install pandas numpy scikit-learn requests
```

## Run

```bash
python app.py
```

The MovieLens dataset (~1MB) downloads automatically on first run.

## Features
- 🔍 Search any movie title for similar recommendations
- 🎬 Browse top movies by genre
- ⭐ Shows ratings and number of reviews
- 📊 Dataset stats panel
- Dark themed GUI