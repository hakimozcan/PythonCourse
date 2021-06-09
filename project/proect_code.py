# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pymc3 as pm
import matplotlib.pyplot as plt
import seaborn as sns
import arviz as az


# PYMC3 INSTALLATION:
    # conda install -c conda-forge pymc3

# DATA SOURCE:
    # https://grensdata.eu/portal.html?_la=nl&_catalog=InterReg&tableId=22003NED&_theme=129



# get the data
border_data = pd.read_csv('~User/OneDrive/QMBU450/PythonCourse/project/Municipal.csv')
border_data['Female'] = border_data['Sex']=='Female'

# one-hot encoding
features_to_encode = ['Nationality', 'Country_of_residence', 'Work_regions'] 
for feature in features_to_encode:
    dummies = pd.get_dummies(border_data[feature], prefix=feature)
    border_data = pd.concat([border_data, dummies],axis=1)

# plot the distribution of sex    
plt.figure(figsize=(12,8))
sns.scatterplot('Periods', 'Sex_%', hue='Female', data=border_data, alpha=0.4);



title_for_plot=''

# the loop is for ploting four different GP figures
for i in range(4):
    
    # the if statements prepare the data for each figure
    if i==0:
        # extract female commuters (predictor) and corresponding percentage values (response)
        X, y = border_data.loc[border_data.Female==True, ['Periods', 'Sex_%']].values.T
        title_for_plot ="Female"
        
    if i==1:
        # a new column for the next step
        border_data['Male'] = border_data['Sex']=='Male'
        # extract male commuters and corresponding percentage values 
        X, y = border_data.loc[border_data.Male==True, ['Periods', 'Sex_%']].values.T
        title_for_plot ="Male"
    
    if i==2:
        # a new column for the next step
        border_data['Belgian'] = border_data['Nationality']=='Belgian'
        # extract Belgian female commuters and corresponding percentage values 
        X, y = border_data.loc[np.logical_and(border_data.Female==True, border_data.Belgian==True), ['Periods', 'Sex_%']].values.T
        title_for_plot ="Female Belgian"
    
    if i==3:
        # a new column for the next step
        border_data['German'] = border_data['Nationality']=='German'
        # extract German female commuters and corresponding percentage values
        X, y = border_data.loc[np.logical_and(border_data.Female==True, border_data.German==True), ['Periods', 'Sex_%']].values.T
        title_for_plot ="Female German"
    
   
   
    #construct a model in PYMC3. PYMC3 uses a context manager to build the model 
    # and automatically add the objects created under context manager to the model
    with pm.Model() as commuting_model:
    
        
        # specify hyperparameters for covariance function 
        ell = pm.Exponential('ell', 1) # determines the variation along X axis
        eta = pm.Exponential('eta', 1) # determines the variation along Y axis.
        
        # covariance function 
        K = eta**2 * pm.gp.cov.ExpQuad(1, ell)  
    
        # radial basis function(?)
        gp = pm.gp.MarginalSparse(cov_func=K, approx="FITC") 
        
        # initialize 5 inducing points with K-means which optimize the location of the points
        Xu = pm.gp.util.kmeans_inducing_points(5, X.reshape(-1,1))
    
        # sigma 
        sig = pm.HalfCauchy("v", beta=1)
        
        #marginal likelihood
        workers = gp.marginal_likelihood("workers", X=X.reshape(-1,1), Xu=Xu, y=y, noise= sig)
        
    #Fit the model 
    with commuting_model:
    
        trace_sex = pm.sample(300, tune=500 )  #TRY FIND.MAP
    
    # Model evaluation (?)
    # plot  the posterior uncertainty in ell, eta, sigma
    # az.plot_trace(trace_sex);
    
    X_range = np.linspace(2009, 2019, 11).reshape(-1, 1)
    
    # conditional prediction
    with commuting_model:
        
        f_pred = gp.conditional('f_pred', X_range)
    
    # posterior   
    with commuting_model:
        
        pred_samples = pm.sample_posterior_predictive(trace_sex, vars=[f_pred], samples=300)
    

    
    # plot the results
    fig = plt.figure(figsize=(8,5))
    ax = fig.gca()
    
    # plot the samples from the gp posterior with samples and shading
    from pymc3.gp.util import plot_gp_dist
    plot_gp_dist(ax, pred_samples["f_pred"], X_range);
    
    # plot the data and the true latent function
    plt.plot(X, y, 'ok', alpha=0.5, label="Observed data");
    plt.plot(Xu, np.ones(Xu.shape[0]), "cx", label="Inducing points")
    
    # axis labels and title
    plt.xlabel("X");
    plt.ylabel("%")
    plt.title(f"Posterior Distribution of {title_for_plot} Commuters"); 

    plt.legend();
    




#REFERENCES:
    # https://www.youtube.com/watch?v=xBE8qdAAj3w&t=2947s&ab_channel=CodingTech
    # Many other publicly available resources 




