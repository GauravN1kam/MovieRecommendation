import streamlit as st
import pickle
import pandas as pd
import requests
import bz2file as bz2

def decompress_pickle(file):

    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

sim = decompress_pickle('simComp.pbz2')
movie_list = pickle.load(open('movies_dict.pkl', 'rb'))
st.title('Movie Recommender System')

movies = pd.DataFrame(movie_list)

selected_movie = st.selectbox('Please Enter movie name', movies['title'].values)




def fetch_image(movie_id):
    responce = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=11fdbc4f7069b6bfcdcea2d0b826f34f&language=en-US'.format(movie_id))
    data = responce.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def Recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sim[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    reccomended_movies = []
    posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from API
        post = fetch_image(movie_id)
        posters.append(post)
        reccomended_movies.append(movies.iloc[i[0]].title)
    return reccomended_movies, posters

if st.button('Recommend'):
    recommcomendation, poster = Recommend(selected_movie)
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.write(recommcomendation[0])
        st.image(poster[0])
    with col2:
        st.write(recommcomendation[1])
        st.image(poster[1])
    with col3:
        st.write(recommcomendation[2])
        st.image(poster[2])
    with col4:
        st.write(recommcomendation[3])
        st.image(poster[3])
    with col5:
        st.write(recommcomendation[4])
        st.image(poster[4])
