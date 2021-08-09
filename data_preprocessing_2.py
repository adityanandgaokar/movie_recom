import pandas as pd
import numpy as np
import ast

credits = pd.read_csv('D:\Projects\Movie_Recommendation_Website\credits.csv')

meta_data = pd.read_csv('D:\Projects\Movie_Recommendation_Website\movies_metadata.csv')

preprocessed_1 = pd.read_csv('D:\Projects\Movie_Recommendation_Website\preprocessed_1.csv')

meta_data['release_date'] = pd.to_datetime(meta_data['release_date'], errors ='coerce')
meta_data['year'] = meta_data['release_date'].dt.year

#only considering movies in 2017
new_meta = meta_data.loc[meta_data.year == 2017, ['genres', 'id', 'title', 'year']]

new_meta['id'] = new_meta['id'].astype(int)

#merging two dataframe using id column
new_df = pd.merge(new_meta, credits, on='id')


new_df['genres'] = new_df['genres'].map(lambda x: ast.literal_eval(x))
new_df['cast'] = new_df['cast'].map(lambda x: ast.literal_eval(x))
new_df['crew'] = new_df['crew'].map(lambda x: ast.literal_eval(x))


def genresList(x):
  cha = ' '
  genre = []

  for i in x:
    if i.get('name') == 'Science Fiction':
      genre.append('Sci-Fi')
    else:
      genre.append(i.get('name'))

  if genre == []:
    return np.NaN

  else:
    return (cha.join(genre))
  


def get_first_actor(x):
  cast = []
  for i in x:
    cast.append(i.get('name'))
  if cast == []:
      return np.NaN
  else:
      return (cast[0])  


def get_second_actor(x):
  cast = []
  for i in x:
    cast.append(i.get('name'))
  if cast == [] or len(cast) <= 1:
      return np.NaN
  else:
      return (cast[1])  



def get_third_actor(x):
  cast = []
  for i in x:
    cast.append(i.get('name'))
  if cast == [] or len(cast) <= 2:
      return np.NaN
  else:
      return (cast[2])


def director_name(x):
  dir = []
  char = ' '
  for i in x:
    if i.get('job') == 'Director':
      dir.append(i.get('name'))
  if dir == []:
    return np.NaN
  else:
    return (char.join(dir))
    





new_df['genres'] = new_df['genres'].map(lambda x: genresList(x))

new_df['actor_1_name'] = new_df['cast'].map(lambda x: get_first_actor(x)) 

new_df['actor_2_name'] = new_df['cast'].map(lambda x: get_second_actor(x)) 

new_df['actor_3_name'] = new_df['cast'].map(lambda x: get_third_actor(x)) 

new_df['director_name'] = new_df['crew'].map(lambda x: director_name(x))


movie_new = new_df.loc[:, ['director_name', 'actor_1_name', 'actor_2_name', 'actor_3_name', 'genres', 'title']]

movie_new = movie_new.rename(columns={'title':'movie_title'})
movie_new['movie_title'] = movie_new['movie_title'].str.lower()

movie_new = movie_new.dropna(how='any')


movie_new['combination'] = movie_new['actor_1_name'] + ' ' + movie_new['actor_2_name'] + ' ' + movie_new['actor_3_name'] + ' ' + movie_new['director_name'] + ' ' + movie_new['genres']

preprocessed_1['combination'] =  preprocessed_1['actor_1_name'] + ' ' + preprocessed_1['actor_2_name'] + ' ' + preprocessed_1['actor_3_name'] + ' ' + preprocessed_1['director_name'] + ' ' + preprocessed_1['genres']

preprocessed_1.head()

preprocessed_2 = preprocessed_1.append(movie_new)

preprocessed_2.drop_duplicates(subset ="movie_title", keep = 'last', inplace = True)

#print(preprocessed_2)

preprocessed_2.to_csv('/content/preprocessed_2.csv', index= False)
