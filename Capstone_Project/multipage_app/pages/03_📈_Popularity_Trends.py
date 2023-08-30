import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

#Popularity trends page

# Dataset: movies2013-2023.csv 
# Graph: Line graph of mean popularity score over the years
# Filters: Genre, isAdult,


st.write("""

# Popularity Trends of Movies

On this page, you can explore how the popularity scores of movies have trended over time. Use the interactive charts below to see the highs and lows of cinematic achievements.


""")



#Loading dataframe
df_path = str(Path(__file__).parents[2] / 'data/movies2013-2023.parquet')
df = pd.read_parquet(df_path)
genre_cols = [col.replace("genre_",'') for col in df.columns if col.startswith('genre_')]


with st.sidebar:
    selector = pd.DataFrame({
        "genre":genre_cols,
        "genre_selection":[True if genre=="Action" else False for genre in genre_cols]
    })


    selector['genre'] = genre_cols
    edited_selector = st.data_editor(selector,\
                                    column_config = {

        "genre":st.column_config.Column(
            label="Genre"

        ),
        "genre_selection": st.column_config.CheckboxColumn(
        label="Select Genre",
        help = "Click on the checkbox to select the genre to be included in the visualization below",
        width="small",
        default=False
        )   
    },
        disabled = ["genre"],
        hide_index=True)

    cols_selected = edited_selector.loc[edited_selector['genre_selection']==True]['genre'].tolist()

    st.session_state.cols_selected = cols_selected #Saves columns selected as a list type

    genres_of_interest = ["genre_"+col for col in st.session_state.cols_selected]

    display_df = pd.DataFrame({"startYear":[num for num in range(2014,2024)]})



    for genre in genres_of_interest:
        gb = df.groupby(['startYear',genre])
        means = gb['popularity_score'].mean().reset_index()
        means.rename(columns={'popularity_score':f"{genre.replace('genre_','')}"}, inplace=True)
        means = means[means[genre]==1].set_index('startYear').drop(genre,axis=1)
        display_df = display_df.merge(means, how='right',left_index=True, right_index=True)

    display_df.index = display_df.index.astype('string')

    if 'startYear' in display_df.columns:
        display_df.drop('startYear',axis=1,inplace=True)

    display_df.reset_index(inplace=True)

    df_melted = display_df.melt(id_vars='startYear', var_name='genre', value_name='popularity_score')


    
    
    
# Define the range for clipping the y-axis
popularity_score_range = [4.5, 7]  # Adjust the range as needed

# Altair chart
chart = alt.Chart(df_melted).mark_line().encode(               
    alt.X('startYear:O'),       # Use 'O' for ordinal if startYear is categorical
    alt.Y('popularity_score:Q', scale = alt.Scale(zero=False)), # Use 'Q' for quantitative
    alt.Color('genre:N'),       # Use 'N' for nominal to differentiate lines by genre
).properties(
    width=600,
    height=400,
    title='Genre Trends over Years'
).interactive()


st.altair_chart(chart,use_container_width=True)
