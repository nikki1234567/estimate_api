# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 14:37:20 2020

@author: nikhi
"""
import pandas as pd
import pickle
from sklearn.cluster import KMeans
import numpy as np
import json

with open('configuration.txt') as json_file:
    config= json.load(json_file)


# df_features  = pd.read_csv('label_features_added.csv')
# df_task = pd.read_csv('label_task_added.csv')
    
df_features  = pd.read_csv(config['dataframe_paths']['LabelFeatureAdded'][1])
df_relation = pd.read_csv(config['dataframe_paths']['relation'][1])
df_task = pd.read_csv(config['dataframe_paths']['LabelTaskAdded'][1])

feature_dictionary = {}

final_features = df_features['Final_Features'].tolist()
final_task = df_task['Final_Features'].tolist()
from feature_mapping import final_list,task_finals,features

# final_list=df_features["Final_Features"].tolist()
# task_finals = df_task['Final_Features'].tolist()
# features =  df_relation['Feature'].tolist()


for ff in final_list:
    for f in ff:
        params = f.split(':')
        try:
            feature_dictionary[params[0].lower()][2]+=1
            feature_dictionary[params[0].lower()][1]+=float(params[1])
            feature_dictionary[params[0].lower()][0].append(float(params[1]))

        except KeyError:
            feature_dictionary[params[0].lower()] = [[],float(params[1]),1]
            feature_dictionary[params[0].lower()][0].append(float(params[1]))

            
    
for tf in task_finals:
    for t in tf:
        part = t.split(':')
        try:
            feature_dictionary[params[0].lower()][2]+=1
            feature_dictionary[params[0].lower()][1]+=float(params[1])
            feature_dictionary[params[0].lower()][0].append(float(params[1]))
        except KeyError:
            feature_dictionary[params[0].lower()] = [[],float(params[1]),1]
            feature_dictionary[params[0].lower()][0].append(float(params[1]))


feature_dictionary1={}      
absent=[]
       
for somef in features:
    if somef not in feature_dictionary.keys():
        absent.append(somef)

with open('featuredictionary.pickle', 'wb') as handle:
    pickle.dump(feature_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)