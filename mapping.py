# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 10:14:11 2020

@author: nikhi
"""


import pandas as pd

df  = pd.read_csv('match_features.csv')
df1 = pd.read_csv('relation-v2.csv')
features_relation = df1['Feature1'].tolist()
final_times = []




for ind in df.index:
    hours = df['ALL_HOURS'][ind]
    actual_features = str(df['Feature_Label'][ind]).split('|')
    times = []
    hours = str(hours).split(',')
    for h in hours:
        # try:
        if str(h).find(':')!=-1:
            split_colon = str(h).split(':')
        else:
            split_colon = str(h).split(' ')
        feature = split_colon[0]
        try:
            time = split_colon[1]
        except IndexError:
            time=0
        original_features = str(df['FEATURES'][ind]).split(',')
        # print(original_features)
        if feature in original_features:
            # print(feature)
            # print(actual_features)
            try:
                act = actual_features[original_features.index(feature)]
            except IndexError:
                continue
            times.append(f'{act}:{time}')
            # print(times)
    final_times.append(times)
                
ct=0              
print(final_times)
for li in final_times:
    if len(li)!=0:
        ct+=1

acc= ct/len(final_times)
print(acc)
           
        # except IndexError:
        #     continue
    