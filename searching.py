# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 15:26:45 2021

@author: nikhi
"""

import pandas as pd
import pickle
import json
import re
# from pattern.en import suggest

with open('configuration.txt') as json_file:
    config= json.load(json_file)


df_relation = pd.read_csv(config['dataframe_paths']['relation'][1])
default_f = pd.read_csv(config['dataframe_paths']['FeatureAddonlist'][1])
with open('featuredictionary1.pickle', 'rb') as handle:
    feature_dictionary = pickle.load(handle)
wordpress_default = []
# project_default = {'Push to staging':4,'Push to production':5,'QA':20,'Hosting and environment setup(local and production)':10,'Planning and analysis':10}
project_default = config['project_default']
for ind in default_f.index:
    if default_f['WordPress Default'][ind]=='D':
        wordpress_default.append(default_f['Featrues'][ind])
        
feature_list = [f for f in wordpress_default]
def reduce_lengthening(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)

# def correction(text):
#     word_wlf = reduce_lengthening(text) #calling function defined above
    
#     correct_word = suggest(word_wlf) 
#     return correct_word


print("Enter the features in the project: ")

f_count=1
    

while True:
    f=int(input("Enter 1 to continue, 0 to exit:"))
    if f==1:
        feat = input(f'Enter Feature {f_count}: ')
        feature_list.append(feat)
        f_count+=1
    elif f==0:
        break

c1_feat = df_relation['Feature'].tolist()
c2_class = df_relation['Synonyms'].tolist()
c3_features = df_relation['Actual_feature'].tolist()
c2_class_split = {}
index =0    
for c in c2_class:
    for x in c.split(','):
        c2_class_split[x.lower().strip()]=index
    index+=1
ans=[]

feature_keys = [x.lower() for x in feature_dictionary.keys()]

def get_hours(fe):
    flag=0
    if fe.lower() in feature_keys:
         return feature_dictionary[fe.lower()]
         # ans.append(feature_dictionary[fe.lower()])

         flag=1
    else:
        for fk in feature_keys:
            keysplit = [y.strip() for y in fk.split(',')]
            if fe.lower() in keysplit:
                return feature_dictionary[fk]
                # ans.append(feature_dictionary[fk])

                flag=1
                
    if flag==1:
        x=0
     
    
    else:
        if fe.lower() in c1_feat:
            ind = c1_feat.index(fe.lower())
            di = feature_dictionary[c3_features[ind].lower()]
            return di
            # ans.append(di)
            
        elif fe.lower() in c2_class_split.keys():
            dic = c3_features[c2_class_split[fe.lower().strip()]] 
            di = feature_dictionary[dic.lower().strip()]
            return di
            # ans.append(di)

        else:
            fe_splt = fe.lower().strip().split(' ')
            possibilities=[]
            itr1=0
            for c1 in c1_feat:
                c1_tok = c1.split(' ')
                if len(fe_splt)==1:
                    li_int = [value for value in fe_splt if value in c1_tok]
                    if len(li_int)!=0:
                        temp=feature_dictionary[c3_features[itr1].lower()]
                        possibilities.append([c3_features[itr1],temp])
                else:
                    if c1_tok[0]==fe_splt[0]:
                        temp=feature_dictionary[c3_features[itr1].lower()]
                        possibilities.append([c3_features[itr1],temp])
                    
                itr1+=1
            itr2=0
            for c2 in c2_class_split.keys():
                c2_tok = c2.split(' ')
                if len(fe_splt)==1:
                    li_int1 = [value for value in fe_splt if value in c2_tok]
                    if len(li_int1)!=0:
                        temp2 = feature_dictionary[c3_features[c2_class_split[c2]].lower()]
                        possibilities.append([c3_features[c2_class_split[c2]],temp2])
                else:
                    if c2_tok[0]==fe_splt[0]:
                        temp2 = feature_dictionary[c3_features[c2_class_split[c2]].lower()]
                        possibilities.append([c3_features[c2_class_split[c2]],temp2])

                itr2+=1
            for c3 in c3_features:
                keysplit1 = [y.strip() for y in c3.split(',')]
                for ks in keysplit1:
                    ks_tok = ks.split(' ')
                    if len(fe_splt)==1:
                        li_int2 = [value for value in fe_splt if value in ks_tok]
                        if len(li_int2)!=0:
                            temp3 = feature_dictionary[c3.lower()]
                            possibilities.append([c3,temp3])
                    else:
                        if ks_tok[0]==fe_splt[0]:
                             temp3 = feature_dictionary[c3.lower()]
                             possibilities.append([c3,temp3])
                         
                        
                
                
            return possibilities
    

for feat_now in feature_list:
    ans.append(get_hours(feat_now))
            

ans_frame1 = list(zip(feature_list,ans))
ans_frame=[]
for it in ans_frame1:
    temp_li =[]
    temp_li.append(it[0])
    temp_li.append(it[1])
    ans_frame.append(temp_li)

    


um_now=[]
for i in range(11,len(feature_list)):
    if isinstance(ans_frame[i][1],list):
        if len(ans_frame[i][1])==0:
            um_now.append(ans_frame[i][0])
  
   
for unmatched_feature in um_now:
    corrected_word = []
    for uf_token in unmatched_feature.split(' '):
        corrected_word.append(reduce_lengthening(uf_token))
    modified_word = ' '.join(corrected_word)
    for entry in ans_frame:
        if entry[0]==unmatched_feature:
            entry[0]=modified_word
            entry[1]=get_hours(modified_word)
    
        
    



        
um=[]
total_hours=0
print('\n***************** Matching features ********************\n')
for i in range(11,len(feature_list)):
    if isinstance(ans_frame[i][1],list):
        if len(ans_frame[i][1])!=0:
            s=0
            for j in range(len(ans_frame[i][1])):
                s+= ans_frame[i][1][j][1]
            s=s/len(ans_frame[i][1])   
            print(f'{ans_frame[i][0].ljust(60)}{round(s,2)}hrs')
            
            total_hours+=round(float(s),2)
        else:
            um.append(ans_frame[i])
    else:
        print(f'{ans_frame[i][0].ljust(60)}{round(float(ans_frame[i][1]),2)}hrs')
        total_hours+=round(float(ans_frame[i][1]),2)

if len(um)!=0:        
    print('\n***************** Unmatched features ********************\n')
    for entry in um:
        print(f'{entry[0].ljust(60)}-')
print('\n***************** Wordpress Default ********************\n')       
for i in range(0,11):
    print(f'{ans_frame[i][0].ljust(60)}{round(ans_frame[i][1],2)}hrs')
    total_hours+=round(ans_frame[i][1],2)
    
print('\n***************** Project Default ********************\n')
total_hours1=0
for k,v in project_default.items():
    if k=='Push to staging':
        val=max(0.5,round((v/100)*total_hours,2))
        print(f'{k.ljust(60)}{val}hrs')
        total_hours1+=val
    elif k=='Push to production':
        val = max(0.5,round((v/100)*total_hours,2))
        print(f'{k.ljust(60)}{val}hrs')
        total_hours1+=val
    elif k=='QA':
        val = max(1,round((v/100)*total_hours,2))
        print(f'{k.ljust(60)}{val}hrs')
        total_hours1+=val
    elif k=='Hosting and environment setup(local and production)':
        val = min(20,round((v/100)*total_hours,2))
        print(f'{k.ljust(60)}{val}hrs')
        total_hours1+=val
    elif k=='Planning and analysis':
        val = max(1,round((v/100)*total_hours,2))
        print(f'{k.ljust(60)}{val}hrs')
        total_hours1+=val
        
    
        
        
        
    
    
#PS min 0.5hrs act 4%
#PtP 5% min 0.5
#QA 20% min 1hr
#HaES 10% max: 20
#plannig and analysis 10% min 1hr

print('\n*************************************************\n')
        
print(f'Total estimated hours: {total_hours+total_hours1} hours')
                  
            
    
        
    