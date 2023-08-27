### Interactive Streamlit interface
I hosted the findings and recommender engines created for this project on Streamlit, a python package that facilitates the development of web apps. [Check it out here!](https://movies-recommender-engine.streamlit.app/)


### Overview

The film industry has historically experienced fluctuations of both booms and busts. However, with the advent of streaming services like Netflix and Disney+, films and movies are continually gaining popularity and more exposure through such streaming services. The author, hence, chose to explore into data revolving the movie industry. 



### Problem Statement

As we usher in an information era, the average consumer is often times overloaded with data and information. From organizations being willing to pay copious amounts of money for online brand visibility through advertisements, to ecommerce/search engines presenting hundreds or even thousands of results with valid search keywords, the importance of distilling and presenting key, relevant information has become more important than ever. Recommender engines play a key role in today's information-rich climate, hence the author chose to explore deeper into the application of recommender engines on the IMDb dataset.


### Datasets

#### Provided Data

There are 2 datasets included in the [`data`](./data/) folder for this project. 

* [IMDb dataset](./data/movies2013-2023.parquet): The IMDb dataset, which is primarily used for data analysis and the cosine similarity recommendation algorithm.
* [Movie Lens 1m dataset](./data/ML1m_merged.parquet): A dataset retrieved from Group Lens, primarily to train a user-based collaborative filtering model


### Recommender Engine

The author created 2 recommender engines (non-personalised attribute based engine, and a user-based collaborative filtering engine), hosted on the 'Recommend Me!' page of the Streamlit application.

#### What goes on under the hood

