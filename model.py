
import pandas as pd
import ast
import os
import requests

# =========================
# OMDb API KEY
# =========================

API_KEY = os.environ.get("OMDB_API_KEY")

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv(
    "movies.csv",
    low_memory=False
)

# Keep important columns
df = df[
    [
        'title',
        'genres',
        'vote_average',
        'overview',
        'homepage',
        'imdb_id'
    ]
]

# Remove empty rows
df.dropna(inplace=True)


# =========================
# EXTRACT GENRES
# =========================

def extract_genres(text):

    genres = []

    try:

        data = ast.literal_eval(text)

        for item in data:

            genres.append(
                item['name'].lower()
            )

    except:

        return ""

    return " ".join(genres)


# Apply extraction
df['genres'] = df['genres'].apply(
    extract_genres
)


# =========================
# FETCH POSTER FROM OMDb
# =========================
def fetch_poster(title):

    url = (
        f"http://www.omdbapi.com/"
        f"?apikey={API_KEY}"
        f"&t={title.replace(' ', '+')}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except requests.RequestException:
        data = {}

    # If poster exists
    if (
        data.get("Poster")
        and data["Poster"] != "N/A"
    ):

        return data["Poster"]

    # Fallback image
    return (
        "https://via.placeholder.com/"
        "300x450?text=No+Poster"
    )
    

# =========================
# RECOMMENDATION FUNCTION
# =========================

def recommend_movies(genre):

    genre = genre.lower().strip()

    # Filter movies
    results = df[
        df['genres'].str.contains(
            genre,
            case=False,
            na=False
        )
    ]

    movies = []

    # Top 30 movies
    for _, row in results.head(30).iterrows():

        movies.append({

            "title": row['title'],

            "poster": fetch_poster(
                row['title']
            ),

            "rating": row['vote_average'],

            # Use the official site when available; otherwise provide IMDb.
            "movie_link": (
                row['homepage']
                if pd.notna(row['homepage']) and row['homepage'].strip()
                else (
                    f"https://www.imdb.com/title/{row['imdb_id']}/"
                    if pd.notna(row['imdb_id']) and row['imdb_id'].strip()
                    else None
                )
            ),

            "description": (
                row['overview']
                if pd.notna(row['overview']) and row['overview'].strip()
                else "Description is not available for this movie."
            )

        })

    return movies
