import streamlit as st
from pathlib import Path

#In this page, write about yourself, your goals, your career ambitions, what this project is about and how this project came about



#Setting title
st.title("About the Author")

col1_intro, col2_intro = st.columns([2,8])

with col1_intro:
    image_path_self1 = Path(__file__).parents[1] / 'images/self1.jpg'
    st.image(image_path_self1)
    

with col2_intro:
    st.markdown("Hello! My name is Brendan, an aspiring data scientist.")
    st.markdown("I first started my data science journey in April 2022, where I first discovered an interest in both writing code that can produce dashboards that can provide business intelligence, as well as creating machine learning models, through a simple online bootcamp.")
    st.markdown("From there, I decided to pursue a data science career, by first equipping myself with data science competencies from a General Assembly bootcamp.")
    st.markdown("In today's climate, technology changes faster than ever. As such, I strongly believe in constantly upskilling and learning, to stay abreast the latest advents in technology and to stay relevant.")



st.markdown("### Skillsets")
st.markdown("The following are some of the skills that I have accumulated along the way:")

col1_skills, col2_skills, col3_skills = st.columns(3)
st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        padding-left:40px;
    }
    </style>
    ''', unsafe_allow_html=True)


with col1_skills:
    st.markdown("**Data Manipulation**")
    st.markdown("-SQL (PostgreSQL)")
    st.markdown("-Numpy/Pandas")
    st.markdown("-statsmodels")
    
with col2_skills:
    st.markdown("**Data Visualization**")
    st.markdown("-matplotlib")
    st.markdown("-seaborn")
    st.markdown("-streamlit")
    

with col3_skills:
    st.markdown("**Machine Learning**")
    st.markdown("-sklearn")
    st.markdown("-XGBoost")
    st.markdown("-Tensorflow/keras")

st.markdown("     ") #Leaving blank lines
st.markdown("     ")


image_skills, desc_skills = st.columns([2,8])

with image_skills:
    image_path_stats_model_for_ml = Path(__file__).parents[1] / 'images/stats_model_for_ml_image.jpg'
    st.image(image_path_stats_model_for_ml)

with desc_skills:
    st.markdown("In the pipelines, I am currently studying on the statistical theories behind the different machine learning models, in order to better understand how these ML models work and have better grounds to tune and optimize the models that I build.")

st.markdown("### About This Project")
st.markdown("While theory is important, I believe it is equally important to put theory to practice. Hence, I built this project as a test of my abilities to incorporate what I have learnt on data manipulation, visualization and alos machine learning, into a web application using streamlit. I also chose to focus on **recommender systems** as my machine learning model of choice (in the page \"Recommend Me!\"), because I can see the growing relevance of **recommender systems** given the increasing abundance of data.")

st.markdown("")





