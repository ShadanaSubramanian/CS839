#Integrating A and B to get table E

import py_entitymatching as em
import pandas as pd
import os, sys
import pandas_profiling
import warnings
import numpy as np
import re
warnings.filterwarnings('ignore')

#Reading A and B

A = em.read_csv_metadata("/mnt/c/Users/sreya/Downloads/DS/bestbuy_music.csv", key= "ID")
B = em.read_csv_metadata("/mnt/c/Users/sreya/Downloads/DS/metacritic_music.csv", key= "ID")

# Setting the Keys
em.set_key(A, 'ID')
em.set_key(B, 'ID')
em.get_property(A, 'key')

#Reading in the Sampled Candidate set (450 tuples) obtained after blocking
G = em.read_csv_metadata("/mnt/c/Users/sreya/Downloads/DS/sampled_candidate_set.csv", key='_id',ltable=A, rtable=B, fk_ltable='ltable_ID', fk_rtable='rtable_ID')

#Split into I and J (train and test)
IJ = em.split_train_test(G, train_proportion=0.7, random_state=0)
I = IJ['train']
J = IJ['test']


#Initializing The matchers


dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='NaiveBayes')

# The features for matching

F = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)

# List the names of the features generated
F['feature_name']

#Extract Feature Vectors.
H = em.extract_feature_vecs(I, 
                            feature_table=F, 
                            attrs_after='Match',
                            show_progress=False)

# compare stats to select best Matcher
#Logistic Regression in our case

result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'],
        k=5,
        target_attr='Match', metric_to_select_matcher='f1', random_state=0)
result['cv_stats']


#Read in the complete candidate set obtained after blocking (973 tuples)
C = em.read_csv_metadata("/mnt/c/Users/sreya/Downloads/candidates_large1.csv", 
                         key='_id',
                         ltable=A, rtable=B, 
                         fk_ltable='ltable_ID', fk_rtable='rtable_ID')
C


K = em.extract_feature_vecs(C, 
                            feature_table=F,
                            show_progress=False)
# Impute feature vectors with the mean of the column values
K = em.impute_table(K, 
                exclude_attrs=['_id', 'ltable_ID', 'rtable_ID'],
                strategy='mean')

# fit with best matcher which was logistic regression
lg.fit(table=H, 
       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
       target_attr='Match')
    
# take best classifier (logistic regression) and output predictions (i.e. matches)
predictions = lg.predict(table=K, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID'], 
                        append=True, target_attr='predicted', inplace=False)


						
						# save set of matches between two tables
matches = predictions.loc[predictions['predicted'] == 1]
matches = matches.loc[:,'_id'].tolist()
mask = C['_id'].isin(matches)
mat = C.loc[mask]
mat.drop_duplicates()
#matches table
mat
#mat.to_csv("matches.csv")

#Splitting the indices of ltable(Metacritic) and rtable(BestBuy)
metacriticMatchInd = [int(s)-1 for s in list(predictions.loc[predictions['predicted'] == 1,'ltable_ID'])]
BBMatchInd = [int(s)-1 for s in list(predictions.loc[predictions['predicted'] == 1,'rtable_ID'])]

#Creating an empty dataframe with columns as in A
E = pd.DataFrame(columns = A.columns[1:])


#merging rtable and ltable values to get E
def mergeTuples(x1, x2):
    t = []
    for i in np.arange(1,len(x1)):
        if A.columns[i] in ['Title','Artist','Genre']:
            if len(x1[i]) >= len(x2[i]):
                curr = x1[i]
                t.append(curr)
            else:
                curr = x2[i]
                t.append(curr)
        if A.columns[i] in ['Release']:
            t.append(x2[i])
        if A.columns[i] in ['Rating']:
            if(x1[i] == 'tbd'):
                t.append(0.0)
            else:
                t.append(float(x1[i]))
    return t


#Calling mergetuples on tuples from BestBuy and Metacritic
for i in np.arange(0,len(BBMatchInd)):
    BBTuple = B.loc[BBMatchInd[i]][0:]
    #print(BBTuple)
    metaTuple = A.loc[metacriticMatchInd[i]][0:]
    #print(metaTuple)
    merged = mergeTuples(BBTuple, metaTuple)
    E.loc[i] = merged

#Merged Table = E
E.to_csv('E.csv')


#Data Analysis:

#Getting the year from Release date
D = E
arr = D['Release'].str.split('/').values
D['Release'] = [s[2] for s in arr]

df_2017 = D.groupby(['Release']).get_group('2017')

#Testing on year 2017
arr1 = df_2017['Genre'].str.split(',').values
lst = []
for val in arr1:
    if any("Rock" in s for s in val):
        if any("Contemporary" in s for s in val):
            lst.append("Contemporary Rock")
        elif any("Alternative" in s for s in val):
            lst.append("Alternative Rock")
        else:
            lst.append("Rock")
    else:
        lst.append('Pop')  
        
df_2017['Genre']  = lst

meanrating = df_2017.groupby('Genre')['Rating'].agg(['count','mean']).reset_index()



#After grouping by year we segregate into different genres (Rock, Alternative, Contemporary and Pop)

def find_Rock(name, group):
    arr1 = group['Genre'].str.split(',').values
    lst = []
    for val in arr1:
        if any("Rock" in s for s in val):
            if any("Contemporary" in s for s in val):
                lst.append("Contemporary Rock")
            elif any("Alternative" in s for s in val):
                lst.append("Alternative Rock")
            else:
                lst.append("Rock")
        else:
            lst.append('Pop')  
    group['Genre']  = lst
    print(name)
    print(group.groupby('Genre')['Rating'].agg(['count','mean']).reset_index())
    print()


grouped = D.groupby(['Release'])
for name, group in grouped:
    find_Rock(name, group)



