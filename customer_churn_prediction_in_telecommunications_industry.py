# -*- coding: utf-8 -*-
"""Customer Churn Prediction in Telecommunications Industry.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1utAaYJWjofS6t0Omx10lWdZFH6hEq6BI

**Install pydrive for data loading**
"""

#Install pydrive to load data
 !pip install -U -q PyDrive

 from pydrive.auth import GoogleAuth
 from pydrive.drive import GoogleDrive
 from google.colab import auth
 from oauth2client.client import GoogleCredentials

 auth.authenticate_user()
 gauth = GoogleAuth()
 gauth.credentials = GoogleCredentials.get_application_default()
 drive = GoogleDrive(gauth)

# copy link and read dataset

link = 'https://drive.google.com/open?id=1J-d61aHgifLIyg2ExPXorC67XBG4P03g'
fluff, id = link.split('=')
file = drive.CreateFile({'id':id}) # replace the id with id of file you want to access
file.GetContentFile('churn.all')

"""**Load Dataset**"""

import io
import pandas as pd
import numpy as np
import imblearn

pd.set_option('display.max_columns', None)
df_churn = pd.read_csv('churn.all')
df_churn.head()

"""Step 1：Data Exploration
1. Dataset Overview (size, datatype, missing values)
2. Features Exploration (correlations)
"""

df_churn.info()

"""Step 2: Feature Preprocessing
1. Observations (missing values, space removal, datatype transfer, corrolations, etc.)
2. categorical features processing (if any/encoding)
"""

df_churn.isnull().sum()

#!pip install pandas-profiling[notebook,html]
!pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip

import pandas_profiling
pandas_profiling.ProfileReport(df_churn)

# Commented out IPython magic to ensure Python compatibility.
# check feature distribution (If Needed)
# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

sns.distplot(df_churn['total_intl_charge'])

"""According to the previous step,  we know that 4 pairs of highly correlated features:

total_day_charge ~ total_day_minutes

total_eve_charge ~ total_eve_minutes 

total_night_charge ~ total_night_minutes 

total_intl_charge ~ total_intl_minutes 
"""

# Drop 'Useless' Features
# Since [area_code(will be roughly represented by State)],[phone_number] are not essential for model training
# [churned] will be the label
to_drop = ['area_code', 'phone_number', 'churned']
churn_tidy = df_churn.drop(to_drop, axis=1)
churn_tidy.head()

churn_tidy['voice_mail_plan'][0]

churn_tidy['intl_plan'][0]

df_churn['churned'][0]

# remove whitespaces in column data

churn_tidy['voice_mail_plan'] = churn_tidy['voice_mail_plan'].map(lambda x: x.strip())
print ('Trimmed [voice_mail_plan]:')
churn_tidy['voice_mail_plan'][0]

# remove whitespaces in column data

churn_tidy['intl_plan'] = churn_tidy['intl_plan'].map(lambda x: x.strip())
print ('Trimmed [intl_plan]:')
churn_tidy['intl_plan'][0]

df_churn['churned'] = df_churn['churned'].map(lambda x: x.strip())
churn_label = np.where(df_churn['churned'] == 'True.', 1, 0)
print ('Trimmed [churned]:')
df_churn['churned'][0]
#churn_label.sum()

# Convert label "churned" to 1; "unchurned" to 0

churn_label = np.where(df_churn['churned'] == 'True.', 1, 0)
#print (str(churn_label))
#np.set_printoptions(threshold=10)
check_label_class = np.unique(churn_label)
print ('label class: '+ str(check_label_class))

# Convert "intl_plan", "voice_mail_plan" into Boolean values.

yes_no_cols = ["intl_plan", "voice_mail_plan"]
churn_tidy[yes_no_cols] = churn_tidy[yes_no_cols] == 'yes'
churn_tidy[yes_no_cols].head()

# Categorical feature processing
# one-hot encoding for feature: "State"

#from category_encoders import *
all_state = churn_tidy['state']
ohe_state = pd.get_dummies(all_state)
ohe_state

# Replace the original feature "state" with "ohe_state"
# Generate new dataset

churn_final = churn_tidy.drop('state', axis = 1)
churn_data = pd.concat([ohe_state, churn_final], axis = 1)
churn_data.info()

"""Step 3: Model Training
1. split dataset
2. model training & selection
"""

# Split Train/Test data

from sklearn import model_selection
X_train, X_test, y_train, y_test = model_selection.train_test_split(churn_data, churn_label, test_size = 0.2)

print ('training data: %d observations; %d features' % X_train.shape)
print ('testing data: %d observations; %d features' % X_test.shape)

# Scale the data using Standardization

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model building

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

# Random Forest
model_RF = RandomForestClassifier()
# K Nearest Neighbors
model_KNN = KNeighborsClassifier()
# Logistic Regression
model_LR = LogisticRegression()

# Model Training/prediction/evaluation

# Random Forest

model_RF.fit(X_train, y_train)
RF_predict = model_RF.predict(X_test)
RF_score = model_RF.score(X_test, y_test)
print ('The accuracy of Random Forest model is %.3f' % RF_score)

# Model Training/prediction/evaluation

# K Nearest Neighbors

model_KNN.fit(X_train, y_train)
KNN_predict = model_KNN.predict(X_test)
KNN_score = model_KNN.score(X_test, y_test)
print ('The accuracy of KNN model is:  %.3f' % KNN_score)

# Model Training/prediction/evaluation

# Logistic Regression

model_LR.fit(X_train, y_train)
LR_predict = model_LR.predict(X_test)
LR_score = model_LR.score(X_test, y_test)
print ('The accuracy of LR model is: %.3f'% LR_score)

# Model Training/prediction/evaluation
# SVM

from sklearn.svm import SVC
model_svc = SVC()
model_svc.fit(X_train, y_train)

svc_predict = model_svc.predict(X_test)
svc_score = model_svc.score(X_test, y_test)
print ('The accuracy of SVC model is: %.3f' %svc_score)

# 5-fold Cross Validation to get the accuracy for each model
model_names = ['Random Forest','KNN','Logistic Regression', 'SVC']
model_list = [model_RF, model_KNN, model_LR, model_svc]
count = 0

for model in model_list:
  cv_score = model_selection.cross_val_score(model, X_train, y_train, cv=5)
  print ('Model Accuracy of %s is: %.3f' % (model_names[count], cv_score.mean()))
  count += 1

# Hyperparameters Tuning
# GridSearch Method
from sklearn.model_selection import GridSearchCV

# Helper function to print results
def print_gs_res(gs):
  print ("Best score: %.3f" % gs.best_score_)
  print ("Best Parameters Set:")
  best_parameters = gs.best_params_ 
  for params_names in sorted(parameters.keys()):
    print ("\t%s: %r" % (params_names, best_parameters[params_names]))

# For Random Forest
# Hyperparameter: Number of Trees
parameters = {'n_estimators': (40, 60, 80)}
Grid_RF = GridSearchCV(RandomForestClassifier(), parameters, cv=5)
Grid_RF.fit(X_train, y_train)

# best number of Trees
print_gs_res(Grid_RF)

best_RF_model = Grid_RF.best_estimator_
best_RF_model

# For KNN
# Hyperparameter: k
parameters = {'n_neighbors': [3,5,7,9]}
Grid_KNN = GridSearchCV(KNeighborsClassifier(), parameters, cv=5)
Grid_KNN.fit(X_train, y_train)

# best k
print_gs_res(Grid_KNN)

best_KNN_model = Grid_KNN.best_estimator_
best_KNN_model

# For Logistic Regression
# Hyperparameter: Penalty choosed from L1 or L2
#                 C: lambda value for L1 and L2
parameters = {'penalty':('l1','l2'), 
              'C': (1,5,10)
              }

Grid_LR = GridSearchCV(LogisticRegression(), parameters, cv=5)
Grid_LR.fit(X_train, y_train)

# best combination
print_gs_res(Grid_LR)

# best LR model
best_LR_model = Grid_LR.best_estimator_
best_LR_model

best_LR_model.coef_[0]

# For best SVM model
# Hyperparameter: Penalty L2
#                 C: lambda value for L2
parameters = {'kernel':('linear', 'rbf', 'poly'), 
              'C': (1,5,10)
              }

Grid_SVC = GridSearchCV(SVC(probability = True), parameters, cv=5)
Grid_SVC.fit(X_train, y_train)

# best combination
print_gs_res(Grid_SVC)

best_SVM_model = Grid_SVC.best_estimator_
best_SVM_model

# Evaluation Metrics
# Accuracy/Precision/Recall

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

# calculate accuracy, precision, recall
def cal_evaluation(classifier, cm):
  tn = cm[0][0]
  fp = cm[0][1]
  fn = cm[1][0]
  tp = cm[1][1]
  accuracy  = (tp + tn) / (tp + fp + fn + tn + 0.0)
  precision = tp / (tp + fp + 0.0)
  recall = tp / (tp + fn + 0.0)
  print (classifier)
  print ("Accuracy is: %0.3f" % accuracy)
  print ("precision is: %0.3f" % precision)
  print ("recall is: %0.3f" % recall)

# print out confusion matrices
def draw_cm(confusion_matrices):
  class_names = ['Not churn', 'Churn']
  for cm in confusion_matrices:
    classifier, cm = cm[0], cm[1]
    cal_evaluation(classifier, cm)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(cm, interpolation='nearest', cmap=plt.get_cmap('Reds'))
    plt.title('Confusion matrix for %s' % classifier)
    fig.colorbar(cax)
    ax.set_xticklabels([''] + class_names)
    ax.set_yticklabels([''] + class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

confusion_matrices = [
                      ('Random Forest', confusion_matrix(y_test, best_RF_model.predict(X_test))),
                      ('Logistic Regression', confusion_matrix(y_test, best_LR_model.predict(X_test))),
                      ('KNN', confusion_matrix(y_test, best_KNN_model.predict(X_test))),
                      ('SVM', confusion_matrix(y_test, best_SVM_model.predict(X_test)))
]

draw_cm(confusion_matrices)

"""Step 4: Model Evaluation


1.   ROC
2.   AUC


"""

# ROC/AUC for Random Forest
from sklearn.metrics import roc_curve
from sklearn import metrics

y_pred_rf = best_RF_model.predict_proba(X_test)[:,1]
fpr_1, tpr_1, _ = roc_curve(y_test, y_pred_rf)
auc_1 = metrics.auc(fpr_1, tpr_1)

y_pred_KNN = best_KNN_model.predict_proba(X_test)[:,1]
fpr_2, tpr_2, _ = roc_curve(y_test, y_pred_KNN)
auc_2 = metrics.auc(fpr_2, tpr_2)

y_pred_LR = best_LR_model.predict_proba(X_test)[:,1]
fpr_3, tpr_3, _ = roc_curve(y_test, y_pred_LR)
auc_3 = metrics.auc(fpr_3, tpr_3)

# ROC of SVM 

y_score = best_SVM_model.fit(X_train, y_train).decision_function(X_test)
fpr_4, tpr_4, _ = roc_curve(y_test, y_score)
auc_4 = metrics.auc(fpr_4, tpr_4)

plt.figure(1)
plt.plot([0,1], [0,1], 'k--' )
plt.plot(fpr_1, tpr_1, 'r', label = 'RF')
plt.plot(fpr_2,tpr_2,'g', label = 'KNN')
plt.plot(fpr_3, tpr_3, 'b', label='LR')
plt.plot(fpr_4,tpr_4, 'y', label = 'SVM')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='best')
plt.show()

print ('\n')
print ('The AUC score of Random Forest model is %.3f'% auc_1)
print ('The AUC score of KNN model is %.3f'% auc_2)
print ('The AUC score of Logistic Regression model is %.3f'% auc_3)
print ('The AUC score of SVM model is %.3f'% auc_4)

# Feature selection discussion
# Check feature importance using Random Forest

rf = RandomForestClassifier()
rf.fit(churn_data, churn_label)

importance = rf.feature_importances_
print ("Feature importance rank: ")
for k,v in sorted(zip(map(lambda x: round(x,4), importance), churn_data.columns), reverse=True):
  print (v + ":" + str(k))