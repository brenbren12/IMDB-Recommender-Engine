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

On this page, you can explore how the popularity scores of movies have trended over time. 

""")



#Loading dataframe
df_path = '../data/movies2013-2023.parquet'
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
    display_df_pop = display_df.copy()
    display_df_pop = display_df.copy()
    


    for genre in genres_of_interest:
        gb = df.groupby(['startYear',genre])
        means_pop = gb['popularity_score'].mean().reset_index()
        means_pop.rename(columns={'popularity_score':f"{genre.replace('genre_','')}"}, inplace=True)
        means_pop = means_pop[means_pop[genre]==1].set_index('startYear').drop(genre,axis=1)
        display_df_pop = display_df_pop.merge(means_pop, how='right',left_index=True, right_index=True)

        

    display_df_pop.index = display_df_pop.index.astype('string')

    if 'startYear' in display_df_pop.columns:
        display_df_pop.drop('startYear',axis=1,inplace=True)

    display_df_pop.reset_index(inplace=True)
    
    df_melted_pop = display_df_pop.melt(id_vars='startYear', var_name='genre', value_name='popularity_score')


    
    
    
# Define the range for clipping the y-axis
popularity_score_range = [4.5, 7]  # Adjust the range as needed

# Altair chart
chart = alt.Chart(df_melted_pop).mark_line().encode(               
    alt.X('startYear:O'),       # Use 'O' for ordinal if startYear is categorical
    alt.Y('popularity_score:Q', scale = alt.Scale(zero=False)), # Use 'Q' for quantitative
    alt.Color('genre:N'),       # Use 'N' for nominal to differentiate lines by genre
).properties(
    width=600,
    height=400,
    title='Genre Trends over Years'
).interactive()


st.altair_chart(chart,use_container_width=True)


# Second chart - Total Volume of Films across the Years
volume_charts = []

for genre in genres_of_interest:
    genre_df = df[df[genre] == 1].groupby('startYear').size().reset_index(name='film_count')
    
    # Altair chart for film count for each genre
    genre_chart = alt.Chart(genre_df).mark_bar().encode(
        alt.X('startYear:O'),
        alt.Y('film_count:Q'),
    ).properties(
        width=300,
        height=200,
        title=f'Total Volume of Films - {genre.replace("genre_", "")}'
    ).interactive()
    
    volume_charts.append(genre_chart)

# Number of columns you want
num_columns = 2

# Split the volume_charts list into sublists with the desired number of columns
split_volume_charts = [volume_charts[i:i + num_columns] for i in range(0, len(volume_charts), num_columns)]

# Concatenate charts in rows with 2 columns
concatenated_charts = alt.vconcat(*[alt.hconcat(*row) for row in split_volume_charts])

# Display the concatenated charts
st.altair_chart(concatenated_charts, use_container_width=True)