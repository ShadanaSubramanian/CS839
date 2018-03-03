import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import svm
from sklearn import tree
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
trainfile = "trainSet.csv"
testfile = "testSet.csv"
df = pd.read_csv(trainfile)
tdf = pd.read_csv(testfile)
n_splits = 10
skf = StratifiedKFold(n_splits, random_state=1)
del df['input']
del tdf['input']
del df['length']
del tdf['length']
#del df['doc']
#del tdf['doc']

#Getting the Test and Train data

#Doing a 10 fold split using StratifiedKFold
y_col = 'person'
target = df[y_col].values
test_target = tdf[y_col].values
del df[y_col]
del tdf[y_col]
train_data = df.values
test_data = tdf.values
skf.get_n_splits(df, target)

#Decision Tree Classfier

decisiontree_classifier = tree.DecisionTreeClassifier()
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    decisiontree_classifier.fit(train_data[train_index],target[train_index])
    y_pred = decisiontree_classifier.predict(train_data[test_index])
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("Decision Tree Classifier: ")
print("\nMax Precision: "+ str(max(precision_list))+ "\nMax Recall: " + str(max(recall_list))+ "\nMax fscore: "+ str(max(fscore_list)) + "\n")

#Linear SVM:
svm_clf = svm.SVC(kernel = 'rbf', random_state = 1, gamma = 0.1, C = 10.0)
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    svm_clf.fit(train_data[train_index],target[train_index])
    y_pred = svm_clf.predict(train_data[test_index])
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("Linear SVM:")
print("\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)) + "\n")

linreg = LinearRegression()
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    linreg.fit(train_data[train_index],target[train_index])
    y_pred = linreg.predict(train_data[test_index])
    thresh = round(np.mean(y_pred), 2)
    y_pred = np.where(y_pred > thresh, 1, 0)
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("Linear Regression")
print("\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)) + "\n")


logreg = LogisticRegression(C = 100.0, random_state = 1)
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    logreg.fit(train_data[train_index],target[train_index])
    y_pred = logreg.predict(train_data[test_index])
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("Logistic Regression")
print("\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)) + "\n")

randomforest = RandomForestClassifier(random_state=1)
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    randomforest.fit(train_data[train_index],target[train_index])
    y_pred = randomforest.predict(train_data[test_index])
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("Random Forest Classifier")
print("\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)) + "\n")

#Best Classifier was Logistic Regression

#Running Logistic Regression on TestSet

logreg = LogisticRegression(C = 100.0, random_state=1)
logreg.fit(train_data, target)
y_pred = logreg.predict(test_data)
precision, recall, fscore ,support = precision_recall_fscore_support(test_target, y_pred, average='macro')
print("Best Classifier : Logistic Regression on Test Set\n")
print("Precision on Test Set: "+ str(precision) +
      "\nRecall on Test Set: "+ str(recall) +
      "\nFScore on Test Set: "+ str(fscore))

