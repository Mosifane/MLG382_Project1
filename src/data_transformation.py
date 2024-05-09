#Data transformation for ml algorithm
import pandas as pd
import numpy as np
from category_encoders import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from pre_proccessing import preproccessing, preproccessing_for_validation
#OHE:
#Gender
#Married
#Education
#Self employed

#Label:
#Property area
#dependents
#credit history
#loan status

#start here
def transformation():
    return (preproccessing().pipe(ohe_columns).pipe(label_encoding))

def transformation_for_validation():
    data_df = preproccessing_for_validation()
    data_df['TotalIncome'] =  data_df['ApplicantIncome'] + data_df['CoapplicantIncome']
    data_df['LoanAmountRatio'] =  data_df['LoanAmount']/data_df['TotalIncome']
    data_df['LoanRepaymentCap'] =  data_df['ApplicantIncome']/data_df['LoanAmount']
    data_df['Loan_Amount_Term'] = np.log(data_df["Loan_Amount_Term"])
    
    return (data_df.pipe(ohe_columns_validation).pipe(label_encoding_validation))

def ohe_columns(data):
    columns_to_ohe = ['Gender', 'Married','Education','Self_Employed']
    ohe = OneHotEncoder(
       use_cat_names = True,
       cols = columns_to_ohe 
    )
    ohe_df = ohe.fit_transform(data)
    return ohe_df

def label_encoding(data):
    #Label:
    #Property_Area
    #Dependents
    #Credit_History
    #Loan_Status
    label_encoding = LabelEncoder()
    columns_to_LE = ['Property_Area', 'Dependents',
                     'Credit_History', 'Loan_Status']
    
    for col in columns_to_LE:
        data[col] = label_encoding.fit_transform(data[col]).astype(int)
    return data

#====================For Validation ====================================================
def ohe_columns_validation(data):
    columns_to_ohe = ['Gender', 'Married','Education','Self_Employed']
    ohe = OneHotEncoder(
       use_cat_names = True,
       cols = columns_to_ohe 
    )
    ohe_df = ohe.fit_transform(data)
    return ohe_df

def label_encoding_validation(data):
    #Label:
    #Property_Area
    #Dependents
    #Credit_History
    #Loan_Status
    label_encoding = LabelEncoder()
    columns_to_LE = ['Property_Area', 'Dependents',
                     'Credit_History']
    
    for col in columns_to_LE:
        data[col] = label_encoding.fit_transform(data[col]).astype(int)
    return data
#print(preproccessing().isnull().sum())
#print(transformation_for_validation().isnull().sum())

