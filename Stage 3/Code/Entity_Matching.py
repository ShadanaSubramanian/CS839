
# coding: utf-8

# In[1]:


import py_entitymatching as em
import pandas as pd
import os, sys
import pandas_profiling
import warnings
warnings.filterwarnings('ignore')


# __Read input tables:__
# We begin by loading the input tables

# In[2]:


A = em.read_csv_metadata("/mnt/c/Users/sreya/Downloads/DS/bestbuy_music.csv",  key= 'ID' )
B = em.read_csv_metadata("/mnt/c/Users/sreya/Downloads/DS/metacritic_music.csv",  key = 'ID')


# In[3]:


em.set_key(A, 'ID')
em.set_key(B, 'ID')
em.get_property(A, 'key')


# __Downsampling:__

# In[4]:


sample_A, sample_B = em.down_sample(A, B, size=50, y_param=1, show_progress=False)


# In[5]:


A.head()


# __Blocking stage:__
# Using OverlapBlocker

# In[6]:


ob = em.OverlapBlocker()


# Blocking on Title with overlap size 1:

# In[7]:


C = ob.block_tables(A, B, 'Title', 'Title', word_level=True, overlap_size=1, rem_stop_words=True, l_output_attrs=['Title', 'Artist', 'Genre'], r_output_attrs=['Title', 'Artist', 'Genre'], show_progress=False)


# Blocking on Artist names with overlap size 1

# In[8]:


C2 = ob.block_candset(C, 'Artist', 'Artist', word_level=True, overlap_size=1, show_progress=False)


# Blocking on Genre using q-grams of size 3 and overlap size 3

# In[9]:


C3 = ob.block_candset(C2, 'Genre', 'Genre', word_level=False, q_val = 3,overlap_size=3, show_progress=False)


# In[10]:


# Candidate_set:
C3


# __Sampling The candidate set:__

# In[11]:


S = em.sample_table(C3, 450)


# In[12]:


S


# __Labelling the Candidate Set:__
# Loading in the Labelled Candidate Set

# In[13]:


G = em.read_csv_metadata("/mnt/c/Users/sreya/Downloads/DS/sampled_candidate_set.csv", key='_id',ltable=A, rtable=B, fk_ltable='ltable_ID', fk_rtable='rtable_ID')


# __Split G into Train and Test for Learning Based Matchers:__

# In[14]:


IJ = em.split_train_test(G, train_proportion=0.7, random_state=0)
I = IJ['train']
J = IJ['test']


# __Initialising Learning Based Matchers for Training:__

# In[15]:


dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='NaiveBayes')


# In[16]:


feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)


# In[17]:


# List the names of the features generated
feature_table['feature_name']


# __Extract Features vectors from Training set I__

# In[18]:


H = em.extract_feature_vecs(I, 
                            feature_table=feature_table, 
                            attrs_after='Match',
                            show_progress=False)


# In[19]:


H.head(3)


# __Run all the Learning Based Matchers to select best one by F1 score:__

# In[20]:


result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'],
        k=5,
        target_attr='Match', metric_to_select_matcher='f1', random_state=0)
result['cv_stats']


# __Best Matchers:__
# 
# Logistic Regression seems to have the Best F1 of 0.98 with the Training set
# 
# Second Best is Decision Trees with an F1 of 0.93

# __Running Matchers on Test Set J:__

# In[21]:


L = em.extract_feature_vecs(J, feature_table=feature_table,
                            attrs_after='Match', show_progress=False)


# __Decision Tree on J:__

# In[22]:


dt.fit(table=H, 
       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
       target_attr='Match')
predictions = dt.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
              append=True, target_attr='predicted', inplace=False)
eval_result = em.eval_matches(predictions, 'Match', 'predicted')
em.print_eval_summary(eval_result)


# __Random Forest on J:__

# In[23]:


rf.fit(table=H, 
       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
       target_attr='Match')
predictions = rf.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
              append=True, target_attr='predicted', inplace=False)
eval_result = em.eval_matches(predictions, 'Match', 'predicted')
em.print_eval_summary(eval_result)


# __SVM on J:__

# In[24]:


svm.fit(table=H, 
       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
       target_attr='Match')
predictions = svm.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
              append=True, target_attr='predicted', inplace=False)
eval_result = em.eval_matches(predictions, 'Match', 'predicted')
em.print_eval_summary(eval_result)


# __Linear Regression on J:__

# In[25]:


ln.fit(table=H, 
       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
       target_attr='Match')
predictions = ln.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
              append=True, target_attr='predicted', inplace=False)
eval_result = em.eval_matches(predictions, 'Match', 'predicted')
em.print_eval_summary(eval_result)


# __Logistic Regression on J:__

# In[26]:


lg.fit(table=H, 
       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
       target_attr='Match')
predictions = lg.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
              append=True, target_attr='predicted', inplace=False)
eval_result = em.eval_matches(predictions, 'Match', 'predicted')
em.print_eval_summary(eval_result)


# __Naive Bayes on J:__

# In[27]:


nb.fit(table=H, 
       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
       target_attr='Match')
predictions = nb.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'Match'], 
              append=True, target_attr='predicted', inplace=False)
eval_result = em.eval_matches(predictions, 'Match', 'predicted')
em.print_eval_summary(eval_result)

