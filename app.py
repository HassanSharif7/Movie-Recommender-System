import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0f7c53fe385985821d818cfe4f13db5e&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = list(movies_df['title']).index(movie)
    distances = similarity[movie_index]
    movies_listz = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_listz:
        movie_id = movies_df.iloc[i[0]]['movie_id']
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_df = pickle.load(open('movie_list.pkl', 'rb'))  # Load as DataFrame
st.title('Movie Recommender System')

# Assuming 'title' is one of the columns in your DataFrame
movies_list = movies_df['title'].values

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies_list
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
