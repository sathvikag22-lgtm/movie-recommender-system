import os

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

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
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

import streamlit as st
import pickle
from huggingface_hub import hf_hub_download

REPO_ID = "sathvikag/movie-recommender-data"

@st.cache_resource
def load_data(filename):
    file_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=filename,
        repo_type="dataset"
    )
    with open(file_path, "rb") as f:
        return pickle.load(f)

movies = load_data("movies.pkl")
movies_dict = load_data("movies_dict.pkl")
similarity = load_data("similarity.pkl")
