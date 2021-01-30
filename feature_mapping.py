# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:14:57 2020

@author: nikhi
"""
import pandas as pd
import json
hours_pat = ['hrs','hours','hour','hr']

with open('configuration.txt') as json_file:
    config= json.load(json_file)

# df_features  = pd.read_csv('label_features.csv')
# df1_relation = pd.read_csv('relation-v2 (1).csv')
# df_task = pd.read_csv('label_task.csv')
    
df_features  = pd.read_csv(config['dataframe_paths']['LabelFeatures'][1])
df1_relation = pd.read_csv(config['dataframe_paths']['relation'][1])
df_task = pd.read_csv(config['dataframe_paths']['labeltask'][1])


task_extracted = df_task['extracted_values'].tolist()
task_labels = df_task['Feature_Label'].tolist()
task_times = df_task['Total_Hours'].tolist()

task_finals = []
features = df1_relation['Feature'].tolist()
synonyms = df1_relation['Synonyms'].tolist()
ind=0
for val in task_extracted:
    val_tokens = str(val).split(',')
    temp_task=[]
    for tok in val_tokens:
        if tok.lower() in features:
            row_tok = df1_relation[df1_relation['Feature']==tok.lower()]
            task_act_features = str(row_tok['Actual_feature'].tolist()[0])
            temp_task.append(f'{task_act_features}:{task_times[ind]}')
    
    ind+=1
    task_finals.append(temp_task)

df_task['Final_Features']=task_finals            
        
st=[]
all_features = []

for ind in df_features.index:
    temp=[]
    all_features.append(str(df_features['FEATURES'][ind]).split(','))
    cur = str(df_features['EXTRACT_HOURS'][ind]).split(' ')
    for i in range(len(cur)):
        if cur[i] in hours_pat:
            context = 7
            s=""
            s+= (cur[i-7]+" "+cur[i-6]+" "+cur[i-5]+" "+cur[i-4]+" "+cur[i-3]+" "+cur[i-2]+" "+cur[i-1]+" "+cur[i])

            temp.append(s)
    st.append(temp)        
    

synonym_features = []
for syn in synonyms:
    temp = syn.split(',')
    synonym_features.append(temp)
    
final_list=[]
not_available=[]
unavailable=set()
index=0

for li in st:
    seen = {}
    
    all_tokens=[]
    for f in li:
        tokens = f.split(" ")
        temp_list=[]
        
        for t in tokens:
            all_tokens.append(t.lower())
            if t.lower() not in features:
                unavailable.add(t)
            if t.lower() in features:
                try:
                    try:
                        seen[t]+=float(tokens[-2])
                    except ValueError:
                        seen[t]+=0
                except KeyError:
                    try:
                        seen[t]=float(tokens[-2])
                    except ValueError:
                        # print(tokens)
                        seen[t]=0
            f_c = 0
            for syn in synonym_features:
                for sy in syn:
                    for s in sy.split(' '):
                    
                        if s.lower()==t.lower():
                            now = df1_relation['Feature'][f_c]
                            try:
                                try:
                                    seen[now]+=float(tokens[-2])
                                except ValueError:
                                    seen[now]+=0
                            except KeyError:
                                try:
                                    seen[now]=float(tokens[-2])
                                except ValueError:
                                    
                                    seen[now]=0
                f_c+=1
                        
            
        for k,v in seen.items():    
            row=df1_relation[df1_relation['Feature']==k]
           
            act_features = str(row['Actual_feature'].tolist()[0])
            
            temp_list.append(f'{act_features}:{v}')
    for something in all_features[index]:
        if something.lower() not in all_tokens:
            not_available.append(something.lower())
    final_list.append(temp_list)
    index+=1
ct=0

for li in final_list:
    if len(li)!=0:
        ct+=1

acc=(ct/len(final_list))*100

not_available_set = set(not_available)
not_present=[]

df_features["Final_Features"]= final_list
df_features["Extractors"] = st

        
        
df_features.to_csv(config['dataframe_paths']['LabelFeatureAdded'][1])
df_task.to_csv(config['dataframe_paths']['LabelTaskAdded'][1])







































# for ind in df_features.index:
#     if len(df_features['Final_Features'][ind])==0:
#         new_list.append(df_features['Extractors'][ind])
