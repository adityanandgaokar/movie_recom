import pandas as pd
import numpy as np
from tmdbv3api import TMDb
import json
import requests
from tmdbv3api import Movie

link = "https://en.wikipedia.org/wiki/List_of_American_films_of_2018"
df1 = pd.read_html(link, header=0)[2]
df2 = pd.read_html(link, header=0)[3]
df3 = pd.read_html(link, header=0)[4]
df4 = pd.read_html(link, header=0)[5]

link = "https://en.wikipedia.org/wiki/List_of_American_films_of_2019"
df5 = pd.read_html(link, header=0)[2]
df6 = pd.read_html(link, header=0)[3]
df7 = pd.read_html(link, header=0)[4]
df8 = pd.read_html(link, header=0)[5]

df = df1.append(df2.append(df3.append(df4,ignore_index=True),ignore_index=True),ignore_index=True)


tmdb = TMDb()
tmdb.api_key = '05134cb28bbd34919fadc768fc18d0f3'
#import imdb
   
# creating instance of IMDb
#ia = imdb.IMDb()



tmdb_movie = Movie()
def get_genre(x):
    genres = []
    
    #popular = tmdb_movie.popular()

    result = tmdb_movie.search(x)
    #search = ia.search_movie(x)

    movie_id = result[0].id
    #print(result)
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data_json = response.json()
    if data_json['genres']:
        genre_str = " " 
        for i in range(0,len(data_json['genres'])):
            genres.append(data_json['genres'][i]['name'])
        return genre_str.join(genres)
    else:
        np.NaN

df['genres'] = df['Title'].map(lambda x: get_genre(str(x)))



df_2018 = df[['Title','Cast and crew','genres']]
df_2018 = df_2018.rename(columns={'Title':'movie_title'})

def director_name(x):
  if " (director)" in x:
        return x.split(" (director)")[0]
  elif " (directors)" in x:
        return x.split(" (directors)")[0]
  else:
        return x.split(" (director/screenplay)")[0]

def first_actor(x):
    return ((x.split("screenplay); ")[-1]).split(", ")[0])


def second_actor(x):
    if len((x.split("screenplay); ")[-1]).split(", ")) < 2:
        return 'unknown'
    else:
        return ((x.split("screenplay); ")[-1]).split(", ")[1])

def third_actor(x):
    if len((x.split("screenplay); ")[-1]).split(", ")) < 3:
        return 'unknown'
    else:
        return ((x.split("screenplay); ")[-1]).split(", ")[2])

df_2018['director_name'] = df_2018['Cast and crew'].map(lambda x: director_name(x))
df_2018['actor_1_name'] = df_2018['Cast and crew'].map(lambda x: first_actor(x))
df_2018['actor_2_name'] = df_2018['Cast and crew'].map(lambda x: second_actor(x))
df_2018['actor_3_name'] = df_2018['Cast and crew'].map(lambda x: third_actor(x))


main_df18 = df_2018.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']]

main_df18['movie_title'] = main_df18['movie_title'].str.lower()

main_df18['combination'] = main_df18['actor_1_name'] + ' ' + main_df18['actor_2_name'] + ' '+ main_df18['actor_3_name'] + ' '+ main_df18['director_name'] +' ' + main_df18['genres']


main_df18

df_new = df5.append(df6.append(df7.append(df8,ignore_index=True),ignore_index=True),ignore_index=True)

df_new['genres'] = df_new['Title'].map(lambda x: get_genre(str(x)))

df_2019 = df[['Title','Cast and crew','genres']]
df_2019 = df_2019.rename(columns={'Title':'movie_title'})


df_2019['director_name'] = df_2019['Cast and crew'].map(lambda x: director_name(str(x)))

df_2019['actor_1_name'] = df_2019['Cast and crew'].map(lambda x: first_actor(x))

df_2019['actor_2_name'] = df_2019['Cast and crew'].map(lambda x: second_actor(x))

df_2019['actor_3_name'] = df_2019['Cast and crew'].map(lambda x: third_actor(x))

main_df19 = df_2019.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']]

main_df19['movie_title'] = main_df19['movie_title'].str.lower()

main_df19['combination'] = main_df19['actor_1_name'] + ' ' + main_df19['actor_2_name'] + ' '+ main_df19['actor_3_name'] + ' '+ main_df19['director_name'] +' ' + main_df19['genres']

my_df = main_df18.append(main_df19,ignore_index=True)

old_df = pd.read_csv('/content/preprocessed_2.csv')

print(old_df)

final_df = old_df.append(my_df,ignore_index=True)

print(final_df)
final_df.isna().sum()

final_df = final_df.dropna(how='any')

final_df.isna().sum()

print('haha')
#final_df.to_csv('/content/preprocessed_3.csv',index=False)
