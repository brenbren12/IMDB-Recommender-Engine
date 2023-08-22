import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("""

# Revenues

The box office speaks volumes about a film's success. Navigate through our revenue analysis to see which movies made a splash financially. Explore data on worldwide revenues, see the trends, and gain insights into the business side of the silver screen.

""")

df = pd.read_csv('../../data/movies2013-2023_castexploded.csv')
revenue = df[df['worldwide_revenue']!=0]


st.sidebar.header('Toggle Parameters here')

def revenue_page_inputs():
    
    pass

fig, ax = plt.subplots(figsize=(10,5))
ax = plt.hist(df['worldwide_revenue'], bins=50, color='skyblue', edgecolor='black')
ax.set_title('Distribution of Worldwide Revenues')
ax.xlabel('Revenue')
ax.ylabel('Number of Movies')
