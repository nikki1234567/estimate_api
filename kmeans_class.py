# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:04:53 2020

@author: nikhi
"""


import pandas as pd
import pickle
from sklearn.cluster import KMeans
import numpy as np
from kneed import KneeLocator
import json

with open('configuration.txt') as json_file:
    config= json.load(json_file)

df = pd.read_csv(config['dataframe_paths']['LabelFeatureAdded'][1])


with open('featuredictionary.pickle', 'rb') as handle:  
    feature_dictionary = pickle.load(handle)

    
def reject_outliers(data):
    
    # p25 = np.percentile(data,25)
    # p75 = np.percentile(data,75)
    # n25=n75=0
    # for x in data.tolist():
    #     if float(x)<=p25:
    #         n25+=1
    #     else if float(x)>=p75:
    #         n75+=1
    
    # if n25>n75:
    p1 = np.percentile(data,10)
    p3 = np.percentile(data,85)
    
    new_data=[]
    
    for x in data.tolist():
        if float(x)>=p1 and float(x)<=p3:
            new_data.append(x)
    
    aft_removal.append(f'{k1}:{new_data} {p1} {p3}')
    return new_data

feature_dictionary1={}

# plot=pd.Series(feature_dictionary['case study management'][0]).plot.box(grid=False,rot=45, fontsize=9)
# plot=pd.Series(feature_dictionary['mailchimp'][0]).plot.bar()

aft_removal = []
convergence =[]



for k1,v in feature_dictionary.items():
    l_30=[]
    m_30=[]
    x = np.array(v[0])
    # if k1=='banner management' or k1=='case study management':
    #     boxplot = pd.Series(x).plot.box(grid=False,rot=45, fontsize=9)
    if len(v[0])>3:
        x = np.array(reject_outliers(x))
        
        
    else:
        x = np.array(v[0])
        aft_removal.append(f'{k1}:{x.tolist()}')
    
    
    if len(set(x.tolist()))>3:
        
        kmeans_kwargs = {
        "init": config['hyperparameters']['init'],
        "n_init": config['hyperparameters']['n_init'],
        "max_iter": config['hyperparameters']['max_iter'],
        "random_state": config['hyperparameters']['random_state'],
        }
    
    # A list holds the SSE values for each k
        sse = []
        num = len(set(x.tolist()))+1
        for k in range(1, len(set(x.tolist()))+1):
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            kmeans.fit(x.reshape(len(x.tolist()),1))
            sse.append(kmeans.inertia_)
        
        
            
        kl = KneeLocator(
            range(1, num), sse, curve="convex", direction="decreasing"
        )
        convergence.append(sse[kl.elbow])
        
        km = KMeans(
            init=config['hyperparameters']['init'],
                n_clusters=kl.elbow,
                n_init=config['hyperparameters']['n_init'],
                max_iter=config['hyperparameters']['max_iter'],
                random_state=config['hyperparameters']['random_state'])
            
        
    else:
         km = KMeans(
            init=config['hyperparameters']['init'],
                n_clusters=1,
                n_init=config['hyperparameters']['n_init'],
                max_iter=config['hyperparameters']['max_iter'],
                random_state=config['hyperparameters']['random_state'])
      
    km.fit(x.reshape(len(x),1))
   
   
    res = max(set(km.labels_), key = km.labels_.tolist().count) 
    ind = 0
    ct=0
    avg=0
    for h in x.tolist():
        if km.labels_[ind]==res:
            avg+=h
            ct+=1
        ind+=1
    
    avg = avg/ct
    l_avg=[]
    for h in x.tolist():
        if h <= avg:
            l_avg.append(h)
    feature_dictionary1[k1]=sum(l_avg)/len(l_avg)
    

with open('featuredictionary1.pickle', 'wb') as handle:
    pickle.dump(feature_dictionary1, handle, protocol=pickle.HIGHEST_PROTOCOL)        


