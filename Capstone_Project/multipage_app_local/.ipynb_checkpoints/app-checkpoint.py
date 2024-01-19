import streamlit as st
from pathlib import Path
import os

#In this page, write about yourself, your goals, your career ambitions, what this project is about and how this project came about



#Setting title
st.title("About the Author")

col1_intro, col2_intro = st.columns([2,8])

with col1_intro:
    
    image_path_self1 = 'C:/Users/tanya/OneDrive/Desktop/IMDB_Recommender_Engine/Capstone_Project/images/self1.jpg'
    st.image(image_path_self1)
    

with col2_intro:
    st.markdown("Hello! My name is [Brendan](https://www.linkedin.com/in/brendan-tan/), and I am passionate about becoming a proficient data scientist.")

    st.markdown("My journey into the world of data science began in April 2022 when I discovered a fascination for crafting code that not only generates insightful dashboards for business intelligence but also drives the creation of powerful machine learning models. This revelation came to me during a simple online bootcamp, igniting a spark of curiosity that would shape my career path.")

    st.markdown("Motivated by this newfound interest, I embarked on my journey to carve out a career in data science. To equip myself with the essential skills and knowledge, I enrolled in a data science program at General Assembly. This intensive experience provided me with the foundational competencies required to excel in the field.")

    st.markdown("In today's rapidly evolving landscape of technology, adaptation is key. I firmly believe in the continuous pursuit of upskilling and learning to remain at the forefront of technological advancements. By staying attuned to the latest breakthroughs, I aim to consistently contribute innovative solutions that address real-world challenges.")

    st.markdown("Please feel free to dive into the projects and insights I've shared!")




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
    image_path_stats_model_for_ml = '../images/stats_model_for_ml_image.jpg'
    st.image(image_path_stats_model_for_ml)

with desc_skills:
    st.markdown("As part of my ongoing learning journey, I am dedicated to deepening my understanding of the statistical theories that underpin various machine learning models. This endeavor allows me to gain a robust foundation, enabling me to fine-tune and optimize the models I construct.")

st.markdown("### About This Project")
st.markdown("While theoretical knowledge forms a strong base, I firmly believe in the value of practical application. This belief drove me to develop this project, showcasing my ability to translate my learnings in data manipulation, visualization, and machine learning into a tangible web application using Streamlit. Notably, I chose to focus on **recommender systems** as my preferred machine learning model (demonstrated in the \"Recommend Me!\" page), given the escalating significance of **recommender systems** in the face of increasing data availability.")

st.markdown("This project reflects my commitment to bridging theory and practice, and serves as a testament to my dedication to honing my skills in data science. By continually seeking opportunities to implement what I learn, I aspire to contribute effectively to the ever-evolving landscape of technology and data-driven solutions.")


st.markdown("")





