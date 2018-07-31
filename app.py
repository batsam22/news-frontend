from flask import Flask,jsonify
from flask_restful import Api, Resource, reqparse
import mysql.connector
import pandas as pd
#news.head();
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from stop_words import get_stop_words
import numpy as np

from flask_cors import CORS



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="JustDial1!",
  database="sources"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT id,date,title,category,chash,language FROM content where language='hi' order by date desc")

myresult = mycursor.fetchall()


app = Flask(__name__)
CORS(app)
api = Api(app)

cols=['id','date','title','category','chash','language']
news=pd.DataFrame(myresult,columns=cols)
news['count']=np.random.randint(0,101,news.shape[0])
news.head()
tfidf = TfidfVectorizer(stop_words=get_stop_words('hindi'))
news['title'] = news['title'].fillna('')
tfidf_matrix = tfidf.fit_transform(news['title'])
tfidf_matrix.shape
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(news.index, index=news['title']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    news2=[(movie_indices[0],news['title'].iloc[0])]

    for i in movie_indices:
        if i==movie_indices[0]:
                continue
        news2.append((i,news['title'].iloc[i]))

#    print(type(news2))

    # Return the top 10 most similar movies
    return news2

test=get_recommendations('LIVE: बारिश से बेहाल मुंबई, सड़कों पर पानी, ट्रेनें भी थमीं')
#test=test.tolist
print(test)


#test=test.to_dict
#test=json.dumps(test.__dict__)
#print(test.id)
#print(test.tolist)



class User(Resource):
    def get(self):
        return (test)


        
      
api.add_resource(User, "/")

app.run(debug=True)
