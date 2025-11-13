import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ----------------------------------------------------------
# Function to download files from Google Drive
# ----------------------------------------------------------
def ensure_file_from_gdrive(local_path: str, file_id: str):
    """Download a file from Google Drive if it's not already present."""
    if os.path.exists(local_path):
        return
    try:
        import gdown
    except ImportError:
        raise RuntimeError("gdown is required. Add 'gdown' to requirements.txt.")

    url = f"https://drive.google.com/uc?id={file_id}"
    st.write(f"Downloading {local_path} from Google Drive...")
    gdown.download(url, local_path, quiet=False)

# ----------------------------------------------------------
# GOOGLE DRIVE FILE IDs (YOUR LINKS)
# ----------------------------------------------------------
SIMILARITY_FILE_ID = "1N_QkrvWqlkkJCNOYzig643YGtMZhZCMt"
MOVIES_FILE_ID = "1eBzyBlzjLcrwTqu3D4wubxQSbi4CGS8I"

# ----------------------------------------------------------
# LOCAL FILENAMES
# ----------------------------------------------------------
SIMILARITY_LOCAL = "similarity.pkl"
MOVIES_LOCAL = "movie_dict.pkl"

# ----------------------------------------------------------
# DOWNLOAD FILES IF MISSING
# ----------------------------------------------------------
ensure_file_from_gdrive(SIMILARITY_LOCAL, SIMILARITY_FILE_ID)
ensure_file_from_gdrive(MOVIES_LOCAL, MOVIES_FILE_ID)

# ----------------------------------------------------------
# LOAD THE FILES
# ----------------------------------------------------------
with open(MOVIES_LOCAL, "rb") as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)

with open(SIMILARITY_LOCAL, "rb") as f:
    similarity = pickle.load(f)

# ----------------------------------------------------------
# POSTER FUNCTION
# ----------------------------------------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=729481c84bed374c6b6d3ca8c34e2fe1&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# ----------------------------------------------------------
# RECOMMENDATION FUNCTION
# ----------------------------------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# ----------------------------------------------------------
# STREAMLIT UI
# ----------------------------------------------------------
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
