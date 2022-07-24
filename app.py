import streamlit as st
import pickle
import pandas as pd
import requests

# All the Functions

# function to fetch detail of selected movie


def fetch_current(movie_id):

    s = 'https://api.themoviedb.org/3/movie/' + \
        str(movie_id[0]) + \
        '?api_key=cf87d15dfc4c7a650bfda39e6b8d754c&language=en-US'

    response = requests.get(s)
    data = response.json()
    poster = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    overview = data['overview']
    rating = data['vote_average']
    release_date = data['release_date']
    genre = data['genres']
    gen = []
    for i in genre:
        gen.append(i['name'])
    genre = ''
    for i in gen:
        genre += i
        genre += '  '

    return poster, overview, rating, release_date, genre


def fetch_cast(movie_id):
    s = 'https://api.themoviedb.org/3/movie/' + \
        str(movie_id[0]) + \
        '/credits?api_key=cf87d15dfc4c7a650bfda39e6b8d754c&language=en-US'
    response = requests.get(s)
    data = response.json()
    cast_names = []
    cast_poster = []
    data = data['cast']
    path = 'https://image.tmdb.org/t/p/w500/'
    for i in range(6):
        cast_names.append(data[i]['original_name'])
        CP = path + data[i]['profile_path']
        cast_poster.append(CP)
    return cast_names, cast_poster


# function to fetch poster of recommeded movies
def fetch_poster(movie_id):

    response = requests.get(
        'https://api.themoviedb.org/3/movie/' + str(
            movie_id) + '?api_key=cf87d15dfc4c7a650bfda39e6b8d754c&language=en-US')
    data = response.json()
    poster = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

    return poster


def fetch_cast_poster(poster_path):
    poster = 'https://image.tmdb.org/t/p/w500/' + 'poster_path'
    return poster


# function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)),
                         reverse=True, key=lambda x: x[1])[1:6]

    recommended_list = []
    poster_paths = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_list.append(movies.iloc[i[0]].title)
        pp = fetch_poster(movie_id)
        poster_paths.append(pp)
    return recommended_list, poster_paths


# loading similarity matrix and data
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


# Building GUI with Streamlit


st.image('header_image.png')


selected_movie_name = st.selectbox(
    'Search Movie',
    movies['title'].values)


intro = '''With the growth of Youtube, Amazon, Netflix, and other similar web services over the last few decades, recommender systems have become increasingly important in our lives. Recommender systems are becoming ubiquitous in our daily online trips, from e-commerce (suggest articles to buyers that may be of interest) to online advertising (suggest the suitable contents to users based on their preferences).
Recommender systems, in a broad sense, are algorithms that try to propose relevant items to consumers (items being movies to watch, text to read, products to buy or anything else depending on industries).
In some industries, recommender systems are critical because they can generate a significant amount of revenue or serve as a way to differentiate yourself from competitors.'''

st.sidebar.title("Movie Recommendation System")
st.sidebar.image('bird1.gif')
st.sidebar.title("Introduction")
st.sidebar.write(intro)
st.sidebar.title('Similarity')
st.sidebar.write('How does it decide which item is most similar to the item user likes? Here we use the similarity scores.It is a numerical value ranges between zero to one which helps to determine how much two items are similar to each other on a scale of zero to one. This similarity score is obtained measuring the similarity between the text details of both of the items. So, similarity score is the measure of similarity between given text details of two items. This can be done by cosine-similarity.')
st.sidebar.title('How Cosine Similarity works?')
st.sidebar.write('Cosine similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance (due to the size of the document), chances are they may still be oriented closer together. The smaller the angle, higher the cosine similarity.')
st.sidebar.image('cosine.png')


if st.button('Recommend'):

    movie_index = movies[movies['title'] == selected_movie_name].index[0]
    current_movie_id = movies[movies['title'] == selected_movie_name].movie_id
    poster, overview, vote, date, genre = fetch_current(
        current_movie_id.values)
    cast_names, cast_poster = fetch_cast(current_movie_id.values)

    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.image(poster, width=230)
    with c2:
        st.subheader('Overview')
        st.write(overview)
        st.write("Genre: " + genre)
        st.write('Rating: ' + str(vote) + '⭐')
        st.write("Release Date: " + str(date))

    st.subheader('Top Cast')
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.image(cast_poster[0])
        st.markdown(cast_names[0])
    with col2:
        st.image(cast_poster[1])
        st.markdown(cast_names[1])
    with col3:
        st.image(cast_poster[2])
        st.markdown(cast_names[2])
    with col4:
        st.image(cast_poster[3])
        st.markdown(cast_names[3])
    with col5:
        st.image(cast_poster[4])
        st.markdown(cast_names[4])
    with col6:
        st.image(cast_poster[5])
        st.markdown(cast_names[5])

    st.subheader('Recommended Movies')

    recom_List, poster_path = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:

        st.image(poster_path[0])
        st.markdown(recom_List[0])
    with col2:

        st.image(poster_path[1])
        st.markdown(recom_List[1])
    with col3:

        st.image(poster_path[2])
        st.markdown(recom_List[2])
    with col4:

        st.image(poster_path[3])
        st.markdown(recom_List[3])
    with col5:

        st.image(poster_path[4])
        st.markdown(recom_List[4])

st.write('Made with ❤️by Keshav Tanwar')
