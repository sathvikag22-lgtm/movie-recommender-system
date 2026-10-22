import streamlit as st
import pickle
import pandas as pd
import requests


import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=db10eb984cd72690a9cfe0dbafa9bf40&language=en-US".format(movie_id)

    response = requests.get(url)
    data = response.json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_posters

movies_dict = pickle.load(open('movies_dict.pkl.','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'How would you like to be contacted?',
movies['title'].values)

if st.button('recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5= st.columns(5)
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

import pickle
import requests
import streamlit as st
import gdown

def load_data(file_id, filename):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    # Check whether Google Drive returned an HTML page
    content_type = response.headers.get("Content-Type", "")

    if "text/html" in content_type.lower():
        st.error(
            f"Google Drive returned an HTML page instead of {filename}. "
            "Check the file ID and sharing permissions."
        )
        st.stop()

    try:
        data = pickle.loads(response.content)
        return data
    except pickle.UnpicklingError:
        st.error(
            f"{filename} is not a valid pickle file. "
            "Check that the Google Drive link points to the correct file."
        )
        st.stop()


MOVIES_ID="12uYE7Fb-XvuGwgj9jMhBLyPk3ThmCLJE"
MOVIES_DICT_ID="1AJbUVb0kdigjhQGcjTqFswxeDhIsDsmy"
SIMILARITY_ID="19AZEHzOtJ7YMGbbI5F0MGaUsThTWxc5V"
movies = load_data(MOVIES_ID, "movies.pkl")
movies_dict = load_data(MOVIES_DICT_ID, "movies_dict.pkl")
similiarity = load_data(SIMILARITY_ID, "similiarity.pkl")

pickle_path = 'movies_dict.pkl'
if not os.path.exists(pickle_path):
    google_drive_url = 'https:\\google.com'

    print("Downloading movies_dict.pkl Google Drive...")
    gdown.download(google_drive_url,pickle_path, fuzzy = True)
movies_dict = pickle.load(open(pickle_path,'rb'))