import sys
import pandas as pd
import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import random
from sklearn.preprocessing import MinMaxScaler
import implicit
import os

os.environ["MKL_NUM_THREADS"] = '1'


def genRecomendation(newdat):
    uid = newdat.loc[0]['user']
    raw_data = pd.read_csv('Sample_df.csv')
    raw_data = pd.concat([raw_data,newdat])
    data = raw_data.dropna()
    data = data.copy()
    data['user'] = data['user'].astype("category")
    data['artist'] = data['artist'].astype("category")
    data['user_id'] = data['user'].cat.codes
    data['artist_id'] = data['artist'].cat.codes
    uid2 = list(data[data['user'] == uid]['user_id'])[0]
    sparse_item_user = sparse.csr_matrix((data['plays'].astype(float), (data['artist_id'], data['user_id'])))
    sparse_user_item = sparse.csr_matrix((data['plays'].astype(float), (data['user_id'], data['artist_id'])))
    model = implicit.als.AlternatingLeastSquares(factors=20, regularization=0.1, iterations=20)
    alpha_val = 15
    data_conf = (sparse_item_user * alpha_val).astype('double')
    model.fit(data_conf)
    user_id = uid2
    print (user_id)
    recommended = model.recommend(user_id, sparse_user_item)
    idxs = []
    artists = []
    scores = []
    for item in recommended:
        idx, score = item
        idxs.append(idx)
        artists.append(data.artist.loc[data.artist_id == idx].iloc[0])
        scores.append(score)
    recommendations = pd.DataFrame({'song_id':idxs,'artist': artists, 'score': scores})
    return recommendations
