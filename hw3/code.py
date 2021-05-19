# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

df = pd.read_csv('~User/OneDrive/QMBU450/PythonCourse/hw3/cses4_cut.csv') 

#Importing column names from the codebook for convenience
verbal_cols=[]
with open('csesCodebook.txt', 'r') as f:
    f = f.readlines()[4:-3]
    for line in f:
         verbal_cols.append(line[29:].rstrip())
df.rename(columns=dict(zip(df.columns[1:], verbal_cols)),inplace=True)


#Initial set of variables selected:
    # GENDER
    # EDUCATION         
    # MARITAL STATUS
    # HOUSEHOLD INCOME
    # RACE
    # RURAL OR URBAN RESIDENCE


# Replacing coded missing values with NaNs

df.replace({'EDUCATION':{97:np.nan, 98:np.nan, 99:np.nan}, \
            'MARITAL STATUS':{7:np.nan, 8:np.nan, 9:np.nan}, \
            'HOUSEHOLD INCOME':{7:np.nan, 8:np.nan, 9:np.nan}, \
            'RURAL OR URBAN RESIDENCE':{9:np.nan}, \
            'RACE':{997:np.nan, 998:np.nan, 999:np.nan}},
               inplace=True)

df.replace({'EDUCATION':{96:0}}, inplace=True) # encoding NO EDUCATION
    
# Replacing NaNs with mode of the column
imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent') 
df1 = pd.DataFrame(imp.fit_transform(df))

# The above-two-lines-code messed the framed data (df). It will be fixed below.
df2=pd.DataFrame(df1)
df2.drop(df2.columns[0:1], inplace = True, axis=1) #droping a extra column
verbal_cols.append("age")
verbal_cols.append("voted")
df2.rename(columns=dict(zip(df2.columns, verbal_cols)),inplace=True) #naming the columns 


# Creating a dataframe of selected variables 
X1 = df2['GENDER']
X2 = df2['EDUCATION']
X3 = df2['MARITAL STATUS']
X4 = df2['HOUSEHOLD INCOME']
X5 = df2['RURAL OR URBAN RESIDENCE']
X6 = df2['RACE']

X = pd.concat([X1, X2, X3, X4, X5, X6], axis=1)

# Extracting the known label
df2['voted'].replace({True:1, False:2}, inplace=True)
y = df2['voted'] 


# One-hot encoding
features_to_encode = [ 'MARITAL STATUS', 'RACE', 'GENDER' ]

for feature in features_to_encode:
    dummies = pd.get_dummies(X[feature], prefix=feature)
    X = X.drop(feature, axis=1)
    X = pd.concat([X, dummies],axis=1)
    

# train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 42)


# Gaussian Naive Bayes

from sklearn.naive_bayes import GaussianNB 
from sklearn.model_selection import  cross_val_score
model = GaussianNB()                       
model.fit(X_train, y_train)                  
ymodel = model.predict(X_test)             
print("accuracy score:", cross_val_score(model, X, y, cv=5).mean())


# Decision Trees and Random Forests

from sklearn.ensemble import RandomForestClassifier
param_grid = {'n_estimators': [500, 1000, 2000]}
grid = GridSearchCV(RandomForestClassifier(random_state=0), param_grid, cv= 5)
grid.fit(X_train, y_train) 
print("tuned hpyerparameters ", grid.best_params_)
print("accuracy score:", grid.best_score_)          #printing accuracy score


# Support Vector Machines

from sklearn.svm import SVC
param_grid = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']} # defining parameter range
grid = GridSearchCV(SVC(random_state=0), param_grid)          #cv default value is 5-fold
grid.fit(X_train, y_train)   # fitting the model for grid search
print("tuned hpyerparameters ", grid.best_params_)
print("accuracy score:", grid.best_score_)          


# Logistic Regression

from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import cross_val_score
model = LogisticRegressionCV(max_iter=1000, random_state=0)
scores = cross_val_score(model, X, y, cv=5).mean()
print(scores)

