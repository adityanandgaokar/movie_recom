from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd



def create_similarity():
  data = pd.read_csv('main_data.csv')

  cv = CountVectorizer()
  print('haha')
  count_matrix = cv.fit_transform(data['combination'])
    # creating a similarity score matrix
  similarity = cosine_similarity(count_matrix)
  return data,similarity




def recom(m):
  m = m.lower()

  #try:
    #data.head()
    #similarity.shape
  #except:
  data, similarity = create_similarity()
  
  if m not in data['movie_title'].unique():
    return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
  else:
    i = data.loc[data['movie_title']==m].index[0]
    lst = list(enumerate(similarity[i]))
    lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
    lst = lst[1:11] # excluding first item since it is the requested movie itself
    l = []
    for i in range(len(lst)):
      a = lst[i][0]
      l.append(data['movie_title'][a])
    #print(l)
    return l

      
#movie = input('enter a movie name : -')

#result = recom(str(movie))



