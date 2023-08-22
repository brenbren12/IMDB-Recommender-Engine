import streamlit as st
import pandas as pd
from annotated_text import annotated_text
import matplotlib.pyplot as plt
from pathlib import Path
import altair as alt

# List down the key findings of your project here. 
# Background
# Datasets Used
# Importing datasets & cleaning
# Exploratory Data Analysis & Visualizations
# Machine Learning
# Conclusions and Recommendations



image_path = str(Path(__file__).parents[2] / 'images/cinema.jpg')

st.image(image_path, use_column_width = True)


#Loading DataFrames--------------------------------------------------------------------------------------------------------##
df_path = str(Path(__file__).parents[2] / 'data/movies2013-2023.parquet')
movielens_1m_path = str(Path(__file__).parents[2] / 'data/ML1m_merged.parquet')
df= pd.read_parquet(df_path).drop(columns=['isAdult','characters'], axis=1)
movielens_1m = pd.read_parquet(movielens_1m_path)

df['startYear'] = df['startYear'].astype('category')



##------------------------------------------------------------------------------------------------------------------------------------------##


st.markdown("""

# Background

**Welcome to the movie analytics web app created with Streamlit.**


"""
)


annotated_text("The film industry has historically experienced fluctuations of both booms and busts. However, with the advent of streaming services like Netflix and Disney+, movies are", ("continually gaining popularity and","","#afa"),(" exposure","","#afa")," through such streaming services. The author, hence, chose to explore into data revolving the movie industry.")


annotated_text("Similarly, with ",("data and information growing in abundance","","#afa",""), 
               "the author sees the value of recommender systems appreciating over time. Therefore, this project is aimed at ")

annotated_text("1. Showcasing an ",("applicative example","","#fea")," on how ",("recommender systems","","#fea")," can be applied to movie and films and")
               
annotated_text("2. Conducting a ",("comprehensive analysis","","#fea")," to ",("uncover trends and insights","","#fea")," of films between 2013 to 2023")

##------------------------------------------------------------------------------------------------------------------------------------------##
##Datasets used
st.markdown(""" 

# Datasets used 

1. The IMDb movie dataset, which was a comprehensive dataset of movie titles, along with movie attributes (such as runtime, year, actors etc) between 2013 to 2023, obtained from the [IMDB Website](https://developer.imdb.com/non-commercial-datasets/). The 'worldwide_revenue' and 'ratings' columns in the dataset were scrapped and merged into the main dataset for analysis purposes. 

""")
st.markdown("This dataset was used primarily for data analysis, and to build the cosine similarity recommender system in the 'Recommend Me!' page.")

st.dataframe(df)
st.caption("IMDb dataset, credits to IMDb")

# st.caption("The above dataframe shows a small substrata of the original dataframe")


st.markdown(""" 

2. The [Movie Lens 1m Ratings and Movies Dataset](https://grouplens.org/datasets/movielens/1m/), which is a publically available dataset with 1 million ratings of movies realsed between 1995 to 2015. This dataset was mainly used for training the user-based collaborative filtering tensorflow model in the 'Recommend Me!' page, due to the availability of ratings for each movie.

""")


st.dataframe(movielens_1m)
st.caption("Movie Lens 1m dataset, credits to GroupLens")


##------------------------------------------------------------------------------------------------------------------------------------------##
st.markdown("""
# Key Insights

The following are the key insights from the data analysis:

1. IMDB has been seeing a **steady decline** in the total number of voters on films year after year. One possible reason is due to increased competition by streaming platforms (eg Netflix, Disney+, Apple TV etc) that also provides web interfaces for exploration of films, similar to that of IMDB.

""")


gb_year = df.groupby('startYear')['numVotes'].sum().reset_index()

st.line_chart(gb_year.set_index('startYear'))




st.markdown("""
2. Genres such as mystery, romance, horror and fantasy has been seeing a gradual increase in viewer popularity recently.

""")


columns_to_drop = ['genres', 'titleType', 'originalTitle', 'runtimeMinutes', 'nconst', 'category', 'job', 'directors', 'writers', 'titleId', 'title', 'region_count']
df2 = df.drop(columns=columns_to_drop)

df_melted = df2.melt(id_vars=['tconst', 'primaryTitle', 'popularity_score', 'startYear'], 
                    value_vars=[col for col in df2.columns if col.startswith('genre_')],
                    var_name='genre', value_name='value')

df_filtered = df_melted[df_melted['value']==1]

gb_genre_startyear = df_filtered.groupby(['genre', 'startYear'])['popularity_score']\
                                .mean()\
                                .reset_index()\
                                .pivot(index='startYear', columns='genre', values='popularity_score')\
                                .reset_index()

gb_genre_startyear = gb_genre_startyear[['startYear','genre_Romance','genre_Mystery',\
                                         'genre_Horror','genre_Fantasy']]



# Altair chart
df_melted2 = gb_genre_startyear.melt(id_vars=['startYear'], value_vars=['genre_Mystery', 'genre_Romance', 'genre_Horror', 'genre_Fantasy'],
                    var_name='genre', value_name='popularity_score')

# Altair chart
alt_chart = alt.Chart(df_melted2).mark_line().encode(
    x='startYear:O',  # Using 'O' type for ordinal scale
    y='popularity_score:Q',  # Using 'Q' type for quantitative scale
    color='genre:N',
    tooltip=['startYear:O', 'popularity_score:Q', 'genre:N']  # Tooltip with additional information
).properties(
    width=600,
    height=400,
    title='Genre Trends over Years'
).interactive()  # Enable interactivity

# Display the Altair chart using st.altair_chart()
st.markdown("### Genre Trends over Years")
st.altair_chart(alt_chart, use_container_width=True)



# plt.figure(figsize=(10, 6))
# plt.plot(gb_genre_startyear['startYear'], gb_genre_startyear['genre_Romance'], label='Romance')
# plt.plot(gb_genre_startyear['startYear'], gb_genre_startyear['genre_Mystery'], label='Mystery')
# plt.plot(gb_genre_startyear['startYear'], gb_genre_startyear['genre_Horror'], label='Horror')
# plt.plot(gb_genre_startyear['startYear'], gb_genre_startyear['genre_Fantasy'], label='Fantasy')
# plt.xlabel('Year')
# plt.ylabel('Popularity Score')
# plt.title('Genre Trends over Years')
# plt.legend()
# plt.show()

# image_stream = io.BytesIO()
# plt.savefig(image_stream, format='png')
# plt.close()

# st.image(image_stream)

# st.line_chart(data=gb_genre_startyear, x='startYear')




st.markdown("""

3. Movies directed by Kenneth Branagh, Ridley Scott, Guy Ritchie, Steven Spielberg, Jaume Collet-Serra and Clint Eastwood earn on average $100m and above in the past 10 years.  

""")


directors_revenue_path = str(Path(__file__).parents[2] / 'data/directors_high_revenue.csv')
directors_revenue = pd.read_csv(directors_revenue_path)

st.bar_chart(data=directors_revenue, x='primaryName', y='adjusted_revenue_in_millions')


# # Create a bar chart using Matplotlib
# plt.figure(figsize=(10, 6))
# directors_revenue.plot(kind='bar')
# plt.xlabel('Director')
# plt.ylabel('Total Adjusted Revenue')
# plt.title('Total Revenue by Director')
# plt.xticks(rotation=45, ha='right') # Rotate the x-axis labels for better visibility

# # Display the plot in Streamlit
# st.pyplot(plt)

