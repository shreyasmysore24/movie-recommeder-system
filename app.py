import pickle
import streamlit as st
from  dotenv import load_dotenv
load_dotenv()
import os
import requests
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_names.append(movie)
    recommended_movie_posters = []
    recc=[]
    for i in distances[1:6]:
        recc.append(movies.iloc[i[0]].title)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
    
    joined = " ".join(recommended_movie_names)
    return joined,recommended_movie_posters,recc

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path




def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    print(response.text)
    return response.text


prompt=["""
        You are an expert in telling the similarity between the starting movie in the list and the rest of the given movies in a small paragraph!
        
\nFor example, \nExamp1e 1 - my question will be "avatar Titan A.E. Aliens vs Predator Falcon Rising Independence Day" here starting movie is avatar your answer should be about 5 movies below the starting movies  like

Titan A.E. (2000): Similar to Avatar's human vs. alien conflict, Titan A.E. features a young man who holds the key to defeating an alien race that destroyed Earth.

Aliens vs Predator: Requiem (2007):  Both "Avatar" and "Requiem" involve human characters caught in the middle of a battle between two powerful alien species. However, Requiem leans more towards action-horror, while Avatar has a stronger focus on environmental themes.

Falcon Rising (1981):  This one deviates a bit. While both involve a protagonist on a foreign world, "Falcon Rising" is a post-apocalyptic story with a lone warrior fighting cyborgs.

Independence Day (1996):  Similar to Avatar's large-scale alien invasion, Independence Day features a global human resistance against a technologically superior alien force.

Aliens (1986):  While "Avatar" focuses on cultural clash, Aliens is a classic sci-fi action film with humans battling a deadly alien species. However, both involve a strong female lead character.
\nExamp1e 2 - john carter
Krrish
Riddick
The Other Side of Heaven
The Legend of Hercules
Get Carter
your answer should be  like 

Krrish: Both John Carter and Krrish feature protagonists with extraordinary abilities on a world different from their own. They fight for good and grapple with fitting in.

Riddick: John Carter and Riddick share elements of science fiction and action. Both have a rugged hero overcoming challenges on a hostile planet. However, Riddick leans darker and more violent.

The Other Side of Heaven: While John Carter is a sci-fi adventure, The Other Side of Heaven is a biographical drama. There's no genre overlap, but both might appeal to viewers who enjoy stories about overcoming adversity in a new environment.

The Legend of Hercules: John Carter and The Legend of Hercules are both action films set in mythical worlds with fantastical elements. They share themes of heroism and defying expectations.

Get Carter: John Carter and Get Carter are complete opposites. John Carter is a sci-fi adventure, while Get Carter is a gritty crime thriller. There's no thematic or genre connection.

also the answer  should not have ''' in the beginning or end and sql word in output
"""]


st.header('Movie Recommender Bot 📽️')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
rec=st.button('Show Recommendation')
if rec:
    recommended_movie_names,recommended_movie_posters,recc= recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recc[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recc[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recc[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recc[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recc[4])
        st.image(recommended_movie_posters[4])

    st.write(get_gemini_response(recommended_movie_names,prompt))
    st.balloons()
    st.snow()