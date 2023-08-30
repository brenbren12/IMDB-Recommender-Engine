### Interactive Streamlit interface
I hosted the findings and recommender engines created for this project on Streamlit, a python package that facilitates the development of web apps. [Check it out here!](https://movies-recommender-engine.streamlit.app/)


### Overview

The film industry has historically experienced fluctuations of both booms and busts. However, with the advent of streaming services like Netflix and Disney+, films and movies are continually gaining popularity and more exposure through such streaming services. The author, hence, chose to explore into data revolving the movie industry. 



### Problem Statement

[The paradox of choice is a phenomenon where an abundance of options can counterintuitively lead to less happiness, less satisfaction, and hamper the ability to make a decision.](https://modelthinkers.com/mental-model/paradox-of-choice#:~:text=The%20paradox%20of%20choice%20is,ability%20to%20make%20a%20decision) 
As we usher in an information era, the average consumer is often times overloaded with data and information and hence, the importance of distilling and presenting key, relevant information has become more important than ever. Recommender engines play a key role in today's information-rich climate, hence I chose to explore deeper into the application of recommender engines, particularly on readily-available datasets such as the IMDb dataset and the Movie Lens 1m dataset.


### Objective of the Project
With the problem statements setting the context of the project, its objectives are therefore to
1. Build recommender engines that can streamline the decision making processes
2. Conduct some exploratory data analysis on the existing datasets to uncover insights that can appeal to stakeholders in the movie industry

T


### Datasets

#### Provided Data

There are 2 datasets included in the [`data`](./Capstone_Project/data/) folder for this project. 

* [IMDb dataset](./data/movies2013-2023.parquet): The IMDb dataset, which is primarily used for data analysis and the cosine similarity recommendation algorithm.
* [Movie Lens 1m dataset](./data/ML1m_merged.parquet): A dataset retrieved from Group Lens, primarily to train a user-based collaborative filtering model


### Recommender Engine

The author created 2 recommender engines (non-personalised attribute based engine, and a user-based collaborative filtering engine), hosted on the 'Recommend Me!' page of the Streamlit application.

#### What goes on under the hood

