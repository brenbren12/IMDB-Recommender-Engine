import pandas as pd
import numpy as np
import os
import re
import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import random


def concat_kaggle_datasets(input_file_list):
    '''
    Concatenates the csv data files retrieved from Kaggle, checks if the csv files all have the same headers,
    then concatenates them rowwise
    
    :param input_file_list: A list of strings with the csv file names, stored inside the "data" folder (eg appletv_title.csv)
    :type input_file_list: list of strings
    
    :return: A tuple of 2 dataframes, first with the titles from all brands concatenated, and the second dataframe with the credit
    details of the actors concatenated
    :rtype: A tuple of 2 DataFrame objects
    
    '''
    
    df_credits = pd.DataFrame(columns=['person_id','id','name','character','role'])
    df_titles = pd.DataFrame(columns = ['id','title','type','description','release_year','age_certification','runtime','genres',\
                            'production_countries','seasons','imdb_id','imdb_score','imdb_votes','tmdb_popularity','tmdb_score'])
    
    for file in input_file_list[1:]:
        print(f"concatting file {file}")
        if file.endswith(".csv"):
            if file.startswith('titles'):
                print(f"df_titles shape: {df_titles.shape}")
                rel_path = '../data/'+file
                df_temp = pd.read_csv(rel_path)
                if df_temp.columns.tolist() != df_titles.columns.tolist():
                    raise Exception(f"Columns of input dataframe from {file} do not match")
                else:
                    df_titles = pd.concat([df_titles, df_temp],axis=0)
                    print(f"df_titles shape aft concat: {df_titles.shape}")

            elif file.startswith('credits'):
                print(f"df_credits shape: {df_credits.shape}")
                rel_path = '../data/'+file
                df_temp = pd.read_csv(rel_path)
                if df_temp.columns.tolist() != df_credits.columns.tolist():
                    raise Exception(f"Columns of input dataframe from {file} do not match")
                else:
                    df_credits = pd.concat([df_credits, df_temp],axis=0)
                    print(f"df_credits shape aft concat: {df_credits.shape}")
            print("="*80)

    return (df_titles, df_credits)


def remove_unusual_characters(text):
    pattern = r'[^a-zA-Z0-9\s]' 
    filtered_text = re.sub(pattern, '', text)
    return filtered_text



def connect():
    return sqlite3.connect("../data/films.db")


# Function to rotate proxies after every 1000 requests
def rotate_proxies(session):
    session._rotate()

# Function to rotate headers after every request
def rotate_headers(headers, current_index):
    next_index = (current_index + 1) % len(headers)
    return headers[next_index], next_index

def get_worldwide_revenue(tconst, proxy):
    '''
    This function scrapes the website www.boxofficemojo.com, and retrieves the worldwide revenue for the tconst value inputted.
    :param tconst: A string of the film id from the imdb database
    :type input_file_list: string
    
    :return: The worldwide revenue from the film with the input film id
    :rtype: integer
    '''
    url = f"https://www.boxofficemojo.com/title/{tconst}/"

    # List of user agent headers
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    ]

    # Initialize header index
    
    try:

        # Set the headers for the request
        headers = {"User-Agent": random.choice(user_agents)}
        
        # Create a session object
        session = requests.Session()
        
        # Set the proxy for the session
        session.proxies = {'http': proxy}
        
        # Make the request using rotating proxies
        res = session.get(url, headers=headers, timeout=5)
        
        if res.status_code == 200:
            print(f"Proxy {proxy} successfully connected")
            soup = BeautifulSoup(res.content, 'html.parser')
            money_tag = soup.find_all('span', class_='money')

            num_values = []

            bold_tag = soup.find_all(name='span', class_='a-size-medium a-text-bold')
            for tag in bold_tag:
                money_tag = tag.find('span', class_='money')
                if money_tag is not None:
                    value = int(money_tag.text.replace('$', '').replace(',', ''))
                    num_values.append(value)
            
            if num_values:
                worldwide_revenue = max(num_values)
                print(f"Worldwide Revenue for {tconst}: ${worldwide_revenue}")
                return worldwide_revenue
            else:
                print(f"No worldwide revenue info provided for {tconst}")
                return 0
        else:
            print(f"Request for {tconst} failed to execute.")

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return 0

    
def get_user_ratings(tconst, proxy):
    
    url = f"https://www.imdb.com/title/{tconst}/reviews"
    
   # List of user agent headers
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    ]

    # Initialize header index
    header_index = 0
    
    rating_and_username = []
    
    try:

        # Set the headers for the request
        headers = {"User-Agent": random.choice(user_agents)}
        
        # Create a session object
        session = requests.Session()
        
        # Set the proxy for the session
        session.proxies = {'http': proxy}
        
        # Make the request using rotating proxies
        res = session.get(url, headers=headers, timeout=5)
        
        if res.status_code==200:
            print(f"Proxy {proxy} successfully connected")
            soup = BeautifulSoup(res.content, 'html.parser')


            chunks = re.findall(pattern = r'<div class="review-container">(.*?)Was this review helpful\?', string=str(soup), flags=re.DOTALL)

            for chunk in chunks:
                if "Warning: Spoilers" in chunk:
                    continue
                else:
                    rating_match = re.search(r'<span>(\d{1})<\/span><span class="point-scale">', chunk)
                    rating = rating_match.group(1) if rating_match else None
                    if rating_match == None:
                        continue

                    username_match = re.search(r'<span class="display-name-link"><a href="\/user\/(.*?)\?ref_=tt_urv', chunk)
                    username = username_match.group(1).strip("/") if username_match else None

                    rating_and_username.append((username, rating))
            
            print(f"Successfully scraped: {rating_and_username}")
            return rating_and_username

        else:
            print(print(f"Request for {tconst} failed to execute."))
            return 0
            
                
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return 0
    
    

    
def get_user_ratings_useridinput(userid, proxy):
    
    url = f"https://www.imdb.com/user/{userid}/ratings"
    
    
   # List of user agent headers
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    ]

    # Initialize header index
    header_index = 0
    
    rating_and_movie = []
    
    try:

        # Set the headers for the request
        headers = {"User-Agent": random.choice(user_agents)}
        
        # Create a session object
        session = requests.Session()
        
        # Set the proxy for the session
        session.proxies = {'http': proxy}
        
        # Make the request using rotating proxies
        res = session.get(url, headers=headers, timeout=5)
        
        if res.status_code==200:
            print(f"Proxy {proxy} successfully connected")
            soup = BeautifulSoup(res.content, 'html.parser')


            chunks = re.findall(pattern = r'<span class="lister-item-index unbold text-primary">(.*?)type="checkbox"/>', string=str(soup), flags=re.DOTALL)

            for chunk in chunks:
                rating_match = re.findall(r'<a href="\/title\/(tt\d+)\/',chunk)
                if len(rating_match)!=1:
                    continue

                movie_id_search = re.findall(r'<span class="ipl-rating-star__rating">(\d{1})</span>',chunk)
                if len(movie_id_search)!=1:
                     continue
                else:
                    rating_and_movie.append((rating_match[0],movie_id_search[0]))

            print(f"Successfully scraped: {rating_and_movie}")
            return rating_and_movie

        else:
            print(print(f"Request for {userid} failed to execute."))
            return 0
            
                
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return 0
    
    
    
