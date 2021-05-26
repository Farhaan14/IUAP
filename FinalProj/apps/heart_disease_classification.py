# -*- coding: utf-8 -*-
"""Heart_disease_Classification.ipynb
"""



# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.construct import random
# %matplotlib inline
import seaborn as sns
import re

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, make_scorer

from plotly.offline import iplot
import plotly as py
import plotly.tools as tls

import pickle

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score


df = pd.read_csv('heart.csv')


df['target'].value_counts()/df.shape[0]*100


# Display age distribution based on heart disease
# sns.distplot(df[df['target'] == 0]['age'], label='Do not have heart disease')
# sns.distplot(df[df['target'] == 1]['age'], label = 'Have heart disease')
# plt.xlabel('Frequency')
# plt.ylabel('Age')
# plt.title('Age Distribution based on Heart Disease')
# plt.legend()
# plt.show()

# pd.crosstab(df.cp,df.target).plot(kind = "bar", figsize = (8, 6))
# plt.title('Heart Disease Frequency According to Chest Pain Type')
# plt.xlabel('Chest Pain Type')
# plt.xticks(np.arange(4), ('typical angina', 'atypical angina', 'non-anginal pain', 'asymptomatic'), rotation = 0)
# plt.ylabel('Frequency')
# plt.show()

target = df['target']
features = df.drop(['target'], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size = 0.2, random_state = 0)

# Train and evaluate model
def fit_eval_model(model, train_features, y_train, test_features, y_test):
    
    """
    Function: train and evaluate a machine learning classifier.
    Args:
      model: machine learning classifier
      train_features: train data extracted features
      y_train: train data lables
      test_features: train data extracted features
      y_test: train data lables
    Return:
      results(dictionary): a dictionary of classification report
    """
    results = {}
    
    # Train the model
    model.fit(train_features, y_train)
    
    # Test the model
    train_predicted = model.predict(train_features)
    test_predicted = model.predict(test_features)
    
     # Classification report and Confusion Matrix
    results['classification_report'] = classification_report(y_test, test_predicted)
    results['confusion_matrix'] = confusion_matrix(y_test, test_predicted)
    results['accuracy'] = accuracy_score(y_test, test_predicted)
        
    return results

sv = SVC(random_state = 1)
# rf = RandomForestClassifier(random_state = 1)
# ab = AdaBoostClassifier(random_state = 1)
gb = GradientBoostingClassifier(random_state = 1)
lr = LogisticRegression(random_state=1)
dt = DecisionTreeClassifier(random_state=1)

# Fit and evaluate models
results = {}
for cls in [sv, dt, gb, lr]:
    cls_name = cls.__class__.__name__
    results[cls_name] = {}
    results[cls_name] = fit_eval_model(cls, X_train, y_train, X_test, y_test)

# Print classifiers results
for result in results:
    print (result)
    print()
    for i in results[result]:
        print (i, ':')
        print(results[result][i])
        print()
    print ('-----')
    print()



importance = gb.feature_importances_
# summarize feature importance
for i,v in enumerate(importance):
    print('Feature: %s, Score: %.5f' % (features.columns[i], v))
# plot feature importance
# plt.bar([x for x in range(len(importance))], importance)
# plt.show()

# Save the model as serialized object pickle
with open('model.pkl', 'wb') as file:
    pickle.dump(gb, file)
