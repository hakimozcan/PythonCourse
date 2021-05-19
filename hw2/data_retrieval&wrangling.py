# -*- coding: utf-8 -*-

# Python 3

"""
This file will look into a dataset obtained from a psychology 
experiment analyzing the relationship between online social support, 
offline social support and mental-wellbeing controling for 
stress level. Data is imported from Qualtrics.

The file contains two functions. The first imporst data and the second
clean the data. The file will not check for the linearity assumptions to focus
on the main requirements of the assignment. However, the assumptions was checked 
using SPSS and they do not appear to be systematically violated.
"""

import requests
import zipfile
import json
import io
import math
import numpy as np
import pandas as pd
import scipy.stats
from ols_function import linear_regression


# The following function imports data using Qualtrics API.
# The code is taken from Qualtrics and slightly modiffied to meet the needs of this assignment.
# The link to the code: https://api.qualtrics.com/guides/docs/Guides/Common%20Tasks/getting-survey-responses-via-the-new-export-apis.md
def exportSurvey():
    
    apiToken = "<my token>"
    surveyId = "<my survey ID>"
    dataCenter = '<my ID>' # "<Organization ID>.<Datacenter ID>"     
    fileFormat = "csv"

    # Setting static parameters
    requestCheckProgress = 0.0
    progressStatus = "inProgress"
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(dataCenter, surveyId)
    headers = {
    "content-type": "application/json",
    "x-api-token": apiToken,
    }

    # Step 1: Creating Data Export
    downloadRequestUrl = baseUrl
    downloadRequestPayload = '{"format":"' + fileFormat + '"}'
    downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
    progressId = downloadRequestResponse.json()["result"]["progressId"]
    print(downloadRequestResponse.text) 

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while progressStatus != "complete" and progressStatus != "failed":
        print ("progressStatus=", progressStatus)
        requestCheckUrl = baseUrl + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        print("Download is " + str(requestCheckProgress) + " complete")
        progressStatus = requestCheckResponse.json()["result"]["status"]

    #step 2.1: Check for error
    if progressStatus is "failed":
        raise Exception("export failed")

    fileId = requestCheckResponse.json()["result"]["fileId"]

    # Step 3: Downloading file
    requestDownloadUrl = baseUrl + fileId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall()
    print('Complete')



# The following function will convert the data from the initial raw form into another
# format which is ready for further analysis.The "list-wise deletion of NaNs" 
# requirement will be handeled under this section.
def dataWrangling(df):
    
    # The 1st step is to drop the unneeded columns 
    df.drop(df.columns[np.r_[0:3, 4:12]], inplace = True, axis=1)

    # The 2nd step to clean and prepare the data for further analysis is 
    # to determine and eliminate those who missed the attention check questions.
    # 33 participants will be eliminated. 
    drop1 = df[ (df['online SS_14'] != 4) | (df['mental wellbeing_10'] != 3) | 
                (df['stress scale_6'] != 3)].index
    df.drop(drop1, inplace = True)
    
    # The 3rd type of respondonts to be eliminated from the dataset is those who
    # filled less than 69% of the survey. 4 participants will be eliminated. 
    drop2 = df[ (df['Progress'] < 69) ].index
    df.drop(drop2, inplace = True)
    
    # The 4th type of respondents to eliminated is those with social-desirability bias. 
    # Theoretically, low social desitabilty score does not pose threat to the results.
    # However,those with a social desirability score higher than the upper bound 
    # of the 95% CI will be eliminated. 
    df['s_desirability_mean_scores'] = df.iloc[:, 64:70].mean(axis=1)  #A new column showing mean social desirability score of each participant
    s_desirability_mean = df['s_desirability_mean_scores'].mean()      #Average of mean social desirability scores
    s_desirability_std = df['s_desirability_mean_scores'].std()        #Std of mean social desirability scores
    z_value = scipy.stats.norm.ppf(1-.05/2) #95% CI z-score (n >30)
    s_desirability_CI_upper = s_desirability_mean + z_value * s_desirability_std #Upper bound of 95% CI. Approximately normally distributed 
    drop3 = df[ df['s_desirability_mean_scores'] > s_desirability_CI_upper ].index
    df.drop(drop3, inplace = True)
    
    # Another step to prepare the data for analysis is to recode reverse-worded items.
    df.replace({'stress scale_5':{1:5, 2:4, 4:2, 5:1},'stress scale_7':{1:5, 2:4, 4:2, 5:1}, \
                 'stress scale_9':{1:5, 2:4, 4:2, 5:1}, 'stress scale_10':{1:5, 2:4, 4:2, 5:1}}, \
               inplace=True)


    df['social_support_mean'] = df.iloc[:, 1:13].mean(axis=1)         #A new column showing mean offline social support score of each participant
    df['online_social_support_mean'] = df.iloc[:, 13:37].mean(axis=1) #A new column showing mean online social support score of each participant
    df['mental_wellbeing_mean'] = df.iloc[:, 37:52].mean(axis=1)      #A new column showing mean mentall wellbeing score of each participant
    df['stress_mean'] = df.iloc[:, 52:64].mean(axis=1)                #A new column showing mean stress score of each participant

    df.to_csv("ProcessedSurveyData.csv")




     
#The function is checked and it works
#exportSurvey() 


# Since the API token and other IDs are personal IDs, they are not provided
# in this file. Instead, the raw data was manually downloaded to
# and imported from a desktop computer.
df1 = pd.read_csv('~User/OneDrive/QMBU450/PythonCourse/hw2/RawSurveyData.csv')

dataWrangling(df1) #Cleans the data

df = pd.read_csv('~User/OneDrive/QMBU450/PythonCourse/hw2/ProcessedSurveyData.csv')

#X1,X2,X3 extracts the IVs from the pre-processed data in df
X1 = df['social_support_mean'] #1st iv of the regression model
X2 = df['online_social_support_mean'] #2nd iv 
X3 = df['stress_mean'] #3rd iv. It is also the control variabale
X0 = pd.Series(1, df.index) #Created for the y-intercepts 
X = pd.concat([X0, X1, X2, X3], axis=1).to_numpy()  #Matrix X 

#Y extracts the DV from the pre-processed data in df
Y = np.array(df['mental_wellbeing_mean']) #Matrix Y 

linear_regression(X, Y)
    


    

    
    

    
    
    

