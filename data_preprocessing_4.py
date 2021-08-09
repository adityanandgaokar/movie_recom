import pandas as pd
import numpy as np
import requests
import bs4 as bs
from six.moves import urllib
from tmdbv3api import TMDb
import json
from tmdbv3api import Movie


link = "https://en.wikipedia.org/wiki/List_of_American_films_of_2020"

source = urllib.request.urlopen(link).read()
soup = bs.BeautifulSoup(source,'lxml')

tables = soup.find_all('table',class_='wikitable sortable')

df1 = pd.read_html(str(tables[0]))[0]
df2 = pd.read_html(str(tables[1]))[0]
df3 = pd.read_html(str(tables[2]))[0]
df4 = pd.read_html(str(tables[3]).replace("'1\"\'",'"1"'))[0] 

df = df1.append(df2.append(df3.append(df4,ignore_index=True),ignore_index=True),ignore_index=True)

print(df)
df_2020 = df[['Title','Cast and crew']]

tmdb = TMDb()
tmdb.api_key = '05134cb28bbd34919fadc768fc18d0f3'

tmdb_movie = Movie() 
def get_genre(x):
    genres = []
    result = tmdb_movie.search(x)
    if not result:
      return np.NaN
    else:
      movie_id = result[0].id
      response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
      data_json = response.json()
      if data_json['genres']:
          genre_str = " " 
          for i in range(0,len(data_json['genres'])):
              genres.append(data_json['genres'][i]['name'])
          return genre_str.join(genres)
      else:
          return np.NaN

df_2020['genres'] = df_2020['Title'].map(lambda x: get_genre(str(x)))


def get_director(x):
    if " (director)" in x:
        return x.split(" (director)")[0]
    elif " (directors)" in x:
        return x.split(" (directors)")[0]
    else:
        return x.split(" (director/screenplay)")[0]


def get_first_actor(x):
    return ((x.split("screenplay); ")[-1]).split(", ")[0])



def get_second_actor(x):
    if len((x.split("screenplay); ")[-1]).split(", ")) < 2:
        return np.NaN
    else:
        return ((x.split("screenplay); ")[-1]).split(", ")[1])


def get_third_actor(x):
    if len((x.split("screenplay); ")[-1]).split(", ")) < 3:
        return np.NaN
    else:
        return ((x.split("screenplay); ")[-1]).split(", ")[2])



df_2020['director_name'] = df_2020['Cast and crew'].map(lambda x: get_director(str(x)))
df_2020['actor_1_name'] = df_2020['Cast and crew'].map(lambda x: get_first_actor(str(x)))
df_2020['actor_2_name'] = df_2020['Cast and crew'].map(lambda x: get_second_actor(str(x)))
df_2020['actor_3_name'] = df_2020['Cast and crew'].map(lambda x: get_third_actor(str(x)))

df_2020 = df_2020.rename(columns={'Title':'movie_title'})

new_df20 = df_2020.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']]

new_df20['combination'] = new_df20['actor_1_name'] + ' ' + new_df20['actor_2_name'] + ' '+ new_df20['actor_3_name'] + ' '+ new_df20['director_name'] +' ' + new_df20['genres']

new_df20.isna().sum()

new_df20 = new_df20.dropna(how='any')

new_df20.isna().sum()

new_df20['movie_title'] = new_df20['movie_title'].str.lower()

old_df = pd.read_csv('/content/preprocessed_3.csv')

final_df = old_df.append(new_df20,ignore_index=True)

print(final_df)

final_df.to_csv('/content/main_data.csv',index=False)