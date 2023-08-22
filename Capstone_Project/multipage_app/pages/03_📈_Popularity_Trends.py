import streamlit as st
import pandas as pd
import altair as alt


#Popularity trends page

# Dataset: movies2013-2023.csv 
# Graph: Line graph of mean popularity score over the years
# Filters: Genre, isAdult,


st.write("""

# Popularity Trends of Movies

Witness the evolution of cinema through the lens of IMDb ratings. On this page, you can explore how the popularity scores of movies have trended over time. Use the interactive charts to see the highs and lows of cinematic achievements, and perhaps discover some timeless classics or hidden gems.


""")



#Loading dataframe
df = pd.read_parquet('../../data/movies2013-2023.parquet')
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


chart = alt.Chart(df_melted).mark_line().encode(               
    alt.X('startYear:O'),                              # Use 'O' for ordinal if startYear is categorical
    alt.Y('popularity_score:Q').scale(zero=False),     # Use 'Q' for quantitative
    color='genre:N',                                   # Use 'N' for nominal to differentiate lines by genre

).properties(
    title='Popularity Score by Genre'
)   


st.altair_chart(chart,use_container_width=True)
