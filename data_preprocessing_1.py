import pandas as pd
import numpy as np

#reading csv file
meta_data = pd.read_csv('D:\Projects\Movie_Recommendation_Website\movie_metadata.csv')

#keeping important columns as features
main_data = meta_data.loc[:, ['director_name', 'actor_3_name', 'actor_2_name', 'actor_1_name', 'genres', 'movie_title']]

#replace string Nan with unknown 
main_data['actor_1_name'] =  main_data['actor_1_name'].replace(np.nan, 'unknown')
main_data['actor_2_name'] =  main_data['actor_2_name'].replace(np.nan, 'unknown')
main_data['actor_3_name'] =  main_data['actor_3_name'].replace(np.nan, 'unknown')

#lowercase all the strings in movie_title colum
main_data['movie_title'] = main_data['movie_title'].str.lower()

main_data['movie_title'] = main_data['movie_title'].apply(lambda x:x[ :-1])

#replace string | with space
main_data['genres'] = main_data['genres'].str.replace('|', ' ')

main_data.to_csv('/content/preprocessed_1.csv', index=False)