import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from imdb import Cinemagoer

from annotated_text import annotated_text
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
from sklearn.metrics.pairwise import cosine_similarity
import tempfile
from pathlib import Path

#Recommender Engine page

## FUTURE IMPROVEMENTS
## 1. Train using ML 20m dataset
## 2. Add a clear cache button


#Instantiating Cinemagoer API
ia = Cinemagoer()

recommender_engine = st.sidebar.selectbox("Select the type of recommender engine below.",\
                                          ('Cosine Similarity',\
                                           'Collaborative Filtering (Tensorflow)'))


# Initialize the state (saved movies list)
if 'saved_movies' not in st.session_state:
    st.session_state.saved_movies = []

if 'saved_movie_id' not in st.session_state:
    st.session_state.saved_movie_id = []
    
    
st.write("""

# Recommend Me!

Welcome to the movie recommender system! As an aspiring data scientist with a passion for machine learning, the author leveraged on cosine similarity, as well as tensorflow, to build this personalized recommendation engine. This tool hopes to serve as a real-world demonstration of how I approach problems and create solutions.

""")



if recommender_engine=='Cosine Similarity':
    st.write("""

    To give you a meaningful recommendation, we will need at least 2 recommendations.

    """)

    st.write("""

    First, please search for a movie (between 2013 to 2022) below. After selecting 2 selections (please do not select duplicate selections), scroll to the bottom of the page where your selections will be saved, and click on Recommend Me!

    """)

    # Setting modal initial state
    modal_state = False
    
    # Search Function
    
    df_path = str(Path(__file__).parents[2] / 'data/movies2013-2023.parquet')
    df = pd.read_parquet(df_path)

    df['primaryTitle'] = df['primaryTitle'].str.title()
    df['originalTitle'] = df['originalTitle'].str.title()

    movie_search = st.text_input("Search movie:",value="", placeholder = "Fast & Furious", ).title()

    N_cards_per_row = 3 #Determines how many cards to show on the page

    #Initializing empty dataframe to show at bottom of page
    df_selection = pd.DataFrame(columns=['Title','Genres','Year Aired', 'Average Rating'])

    if movie_search:
        mask_primary = df["primaryTitle"].str.contains(movie_search)
        mask_original = df["originalTitle"].str.contains(movie_search)
        df_search = df[mask_primary | mask_original]

        for n_row, row in df_search.reset_index().iterrows():
            i = n_row%N_cards_per_row
            if i==0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
            # draw the card
            with cols[n_row%N_cards_per_row]:
                id = row['tconst']
                id_without_tt = id.replace('tt','')

                link = f"https://www.imdb.com/title/{id}/"
                st.markdown(f"**[{row['primaryTitle']}]({link})**")

                st.markdown(f"{row['genres']}")
                st.markdown(f"Year Aired: {row['startYear']}")
                 # Add a save button to save the movie
                if st.button(f"Select {row['primaryTitle']}", key=f"button_{row['tconst']}"):
                    if row['tconst'] in st.session_state.saved_movie_id:
                        st.error("Selection already exists")
                    else:
                        modal = Modal(key="Successful Selection",title="Successful Selection")
                        st.session_state.saved_movies.append(row['primaryTitle'])
                        st.session_state.saved_movie_id.append(row['tconst'])
                        modal_state = True
                        
                    while modal_state:
                        modal.open()
                        if modal.is_open():
                            st.markdown(f"You have selected {row['primaryTitle']}. Check the data table below to see your selection")
                            
                        
                        

    # Instantiating empty list to store movie IDs
    selected_movie_ids = []

    # Display saved movies
    st.write("Selected Movies:")


    for movie in st.session_state.saved_movie_id:
        selected_movie_ids.append(movie)
        row_values = {'Title': df[df['tconst']==movie]['originalTitle'],
                     'Genres': df[df['tconst']==movie]['genres'],
                     'Year Aired': df[df['tconst']==movie]['startYear'],
                     'Average Rating': df[df['tconst']==movie]['averageRating']}
        df_selection = pd.concat([df_selection, pd.DataFrame(row_values)])

    st.dataframe(df_selection, use_container_width=True)


    #Loading different recommendation dataset
    rec_df_path = str(Path(__file__).parents[2] / 'data/movies2013-2023_MF.parquet')
    rec_df = pd.read_parquet(rec_df_path)\
            .drop_duplicates('tconst')\
            .set_index('tconst')
    rec_df = rec_df.fillna('')



    if st.button(f"Recommend Me!"):
        if len(df_selection)==0:
            st.error("Please select 2 movies!")
        elif len(df_selection)==1:
            st.error("Please select 1 more movie")
        else:
            watched_movie_ids = st.session_state.saved_movie_id

            watched_features = rec_df[rec_df.index.isin(watched_movie_ids)].drop(['primaryTitle', 'popularity_score', 'recommendation_propensity'], axis=1)

            features = rec_df.drop(['primaryTitle', 'popularity_score', 'recommendation_propensity'], axis=1)

            similarity_to_watched = cosine_similarity(features, watched_features)
            average_similarity = similarity_to_watched.mean(axis=1)

            # Set the similarity of watched movies to a low value
            average_similarity[rec_df.index.isin(watched_movie_ids)] = -1

            # Get the indices of the movies with the top 5 highest average similarity
            recommended_indices = average_similarity.argsort()[-20:][::-1]

            # Get the movie IDs of the recommended movies
            recommended_movie_ids = rec_df.index[recommended_indices]
            recommended_movies = rec_df.loc[recommended_movie_ids].sort_values(['recommendation_propensity','averageRating'],ascending=False)
            recommended_movies = recommended_movies[recommended_movies['averageRating']>=5]
            recommended_movies = recommended_movies.iloc[:3]

            if len(recommended_movies) == 0:
                st.write("Your taste is very unique! We are not able to find a suitable recommendation for you")

            else:


                st.write(""" We recommend the following movies: """)
                # st.dataframe(recommended_movies) #Show dataframe for debugging purposes

                #Showing top recommendations in cards:
                for n_row, row in recommended_movies.reset_index().iterrows():
                    i = n_row%N_cards_per_row
                    if i==0:
                        st.write("---")
                        cols = st.columns(N_cards_per_row, gap="large")
                # draw the card
                    with cols[n_row%N_cards_per_row]:
                        id = row['tconst']
                        id_without_tt = id.replace('tt','')
                        link = f"https://www.imdb.com/title/{id}/"
                        st.markdown(f"**[{row['primaryTitle']}]({link})**")
                        movie = ia.get_movie(id_without_tt)
                        poster_url = movie.get('full-size cover url')
                        st.image(poster_url)

    

#-----------------------------------------------------------------------------------------------------------------------------------------------#
elif recommender_engine=='Collaborative Filtering (Tensorflow)':
    df_path = str(Path(__file__).parents[2] / 'data/ML1m_merged.parquet')
    df = pd.read_parquet(df_path)
    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0", axis=1,inplace=True)
    
    st.markdown("**The Author used the Movie Lens 1m dataset, together with keras (tensorflow), to train this user-based collaborative filtering model.**")
    st.markdown("The following is the dataset used:")
    st.dataframe(df)
    
    model_path = str(Path(__file__).parents[2]/'models/reco_v2.h5')
    model = tf.keras.models.load_model(model_path)
    plot_path=str(Path(__file__).parents[2]/'images/model.jpg')
    st.markdown("And the following is the model architecture:")
    st.image(plot_path, caption="Model Architecture")
    st.caption("This collaborative filtering model was trained using keras, with a validation MSE of 0.94.")
    
    annotated_text("The model takes 2 inputs: a", ("user index","","#fea"), \
                   "and a ", ("movie index","","#afa"),\
                  "which is then passed through the model in several layers.")
    st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        padding-left:40px;
    }
    </style>
    ''', unsafe_allow_html=True)
    st.markdown("The first are the respective embedding layers to convert the inputs into tensors. The author chose 5 as the number of latent dimensions for the model, considering the following dimensions of considerations while rating a movie:")
    
    st.markdown("- Genre")
    st.markdown("- Actors")
    st.markdown("- Directors")
    st.markdown("- Length of Movie")
    st.markdown("- Average Rating")

    st.markdown("Next, the embedding layers are flattened and then concatenated together.")
    st.markdown("The inputs are then put through a series of 2 Dense hidden layers, alternated with dropout layers of 0.5 ratio, before normalizing the outputs from the last hidden Dense layer and then passed through a ReLu activation function.")






#st.session_state.saved_movie_id output when selecting a movie
# [
#   "tt2820852"
# ]



