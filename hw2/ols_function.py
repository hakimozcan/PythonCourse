# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import math
import scipy.stats



def linear_regression(X, Y):
    #check empty input array
    assert Y.shape[0] > X.shape[1] > 0 
    #check for zeroDivision when finding variance
    assert (Y.shape[0] - X.shape[1]) > 0
    
    # checks if the given inputs are type of array
    if not isinstance(X, np.ndarray) or not isinstance(Y, np.ndarray):
        raise TypeError("Given inputs should be array")
    
    # checks if X has at least 3 variables the including conrol variable and ones for y-intercept  
    if not X.shape[1] > 2:
        raise ValueError("Given input array for IVs should iclude at least 3 columns.")
    
    # checks if Y has at most 1 variable
    if not Y.size/Y.shape[0] < 2:
        raise ValueError("Given input array for DV should include at most 1 column.")
    
    # checks if X.T can be multiplied with Y
    if X.shape[0] != Y.shape[0]:
        raise ValueError("Given inputs(matricies) does not match for multiplication")
    
    # checks if given input arrays have non-numeric values
    if ("float" or "int") not in (str(X.dtype) or str(Y.dtype)):
        raise TypeError("Given inputs should be numeric arrays")
    
    #check for underdetermined system of equations, zeroDivision and empty dataset
    if X.shape[0] < X.shape[1]:
        raise AttributeError("Given input arrays lead to an underdetermined system of equations")
        

    #columns=["X0","X1","X2","X3","Y"]
    df1=pd.concat([pd.DataFrame(X),pd.DataFrame(Y)], axis=1,) #merges covariates and DV
    df1[~np.isnan(df1).any(axis=1)] #perform listwise deletion of NaNs
    X1 = np.array(df1.iloc[:,:-1]) #split covariates from df1 and psyc wellbeing is DV
    Y1 = np.array(df1.iloc[:,-1:]).reshape(135,) # split DV from df1 and psyc wellbeing is DV
    
    # stress is originally a mediator variable but one hypothesis require it to be also evaluated as DV
    X2 = np.array(df1.iloc[:,:-2]) #split covariates from df1 and now stress is DV
    Y2 = np.array(df1.iloc[:,-2:-1]).reshape(135,) ##split DV from df1 and stress is DV
    
    X = [X1, X2] # IVs respectively for psyc wellbeing and stress as DV
    Y = [Y1, Y2] # psyc wellbeing and stress
    lst=[]
    
    # the following function regress the data both when psyc wellbeing and stress is DV
    for X, Y in zip(X, Y):
        #finds β value that minimize the sum of squared errors(e.T @ e)
        B = np.linalg.inv(X.T @ X) @ (X.T @ Y) 
        e = Y - (X @ B) #calculates the error term
        var = (e.T @ e) / (len(X) - len(X[1])) #len(X[1] coressponds to k +1 (dimensional space)
        B_var = np.diag(var * np.linalg.inv(X.T @ X))
        B_SE = np.sqrt(B_var/len(X)) 
        t = scipy.stats.t.ppf(1-.05/2, len(X) - len(X[1]))                   
        B_U_CI = B + t*B_SE #CI upper bound
        B_L_CI = B - t*B_SE #CI lower bound
    
        lst.append([B,B_SE,B_U_CI,B_L_CI])
    
    
    df1=pd.DataFrame(lst[0], index=["B","B_SE","B_U_CI","B_L_CI"], columns=["B0","SocialSupport","OnlineSocialSupport","Stress"])
    df2=pd.DataFrame(lst[1], index=["B","B_SE","B_U_CI","B_L_CI"], columns=["B0","SocialSupport","OnlineSocialSupport"]) 
    
    print ("\nβ, SE, CI when Wellbeing is DV:\n\n",df1, "\n\n\nβ, SE, CI when Stress is DV:\n\n", df2 )
        
        

     
    
    
    
    

    