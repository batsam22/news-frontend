from flask import Flask
import rec as f
app = Flask(__name__)
import pandas as pd
#news.head();
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@app.route('/<title>')
def hello_name(title):

	cols=['id','date','title','category','chash','language'];
	news=pd.read_csv('./news.csv',sep=',', names=cols,encoding='latin-1');
	news['count']=np.random.randint(0,101,news.shape[0])
	news.head();
	tfidf = TfidfVectorizer(stop_words='english')
	news['title'] = news['title'].fillna('')
	#title
	tfidf_matrix = tfidf.fit_transform(news['title'])
	tfidf_matrix.shape
	cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
	indices = pd.Series(news.index, index=news['title']).drop_duplicates()

	#category
	count = CountVectorizer(stop_words='english')
	count_matrix = count.fit_transform(news['chash'])
	
	cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
	news= news.reset_index()
	indices = pd.Series(news.index, index=news['title'])


	# Get the index of the movie that matches the title
	idx = indices[title]
	# Get the pairwsie similarity scores of all movies with that movie
	sim_scores = list(enumerate(cosine_sim[idx]))
	# Sort the movies based on the similarity scores
	sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
	# Get the scores of the 10 most similar movies
	sim_scores = sim_scores[1:21]
	# Get the movie indices
	movie_indices = [i[0] for i in sim_scores]
	# Return the top 10 most similar movies
	return news['title'].iloc[movie_indices]






if __name__ == '__main__':
   app.run(debug = True)
