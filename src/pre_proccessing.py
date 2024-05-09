import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def load_data():
    #load the data just move 1 folders out of current dir
    raw_data_df = pd.read_csv("././data/raw_data.csv")
   
    return raw_data_df

def load_data_for_validation():
    #load the data just move 1 folders out of current dir
    raw_data_df = pd.read_csv("././data/validation.csv")
   
    return raw_data_df

def loanAmount(raw_data_df):
    
    #fill missing values with mean
    raw_data_df['LoanAmount'].fillna(
        raw_data_df['LoanAmount'].mean(), inplace=True
    )

    #find the quartile ranges to identify outliers
    Q1= raw_data_df['LoanAmount'].quantile(0.25) 
    Q3= raw_data_df['LoanAmount'].quantile(0.75)

    inter_quartile_range = Q3-Q1

    #find the inter quartile ranges
    lower_bound = Q1 - (1.5*inter_quartile_range)
    upper_bound = Q3 + (1.5*inter_quartile_range)

    #isolate outliers
    outliers_indexes = []

    for index, row in enumerate(raw_data_df['LoanAmount']):
        if row < lower_bound:
            outliers_indexes.append(index)
        else:
            if row > upper_bound:
                outliers_indexes.append(index)  

    #removing Outliers
    #Drop the whole rows with outliers 
    raw_data_df.drop(outliers_indexes, inplace=True)
    return raw_data_df

#preproccess Self_Employed
def self_Employed(data_df):
    #fill missing values using mode of self employed
    data_df['Self_Employed'] = data_df['Self_Employed'].fillna(data_df['Self_Employed'].mode()[0])
    return data_df

#preproccess Loan Amount term
def loan_amount_term(data):
    # Replace the missing the data with the most frequent data in months
    frequentVal = data['Loan_Amount_Term'].mode().values[0]

    # Replace the NaN values with the frequent val:
    data['Loan_Amount_Term'].fillna(frequentVal, inplace=True)
    return data

# Applicant Income
def applicant_income(data):
    
    #Outliers handling
    # Remove outliers of ApplicantIncome
    Q1 = data['ApplicantIncome'].quantile(0.25)
    Q3 = data['ApplicantIncome'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_mask = (data['ApplicantIncome'] > lower_bound) & (data['ApplicantIncome'] < upper_bound)

    data = data[outlier_mask]
    return data

#Credit History
def Credit_History(raw_data_df):
    # replace empty rows with the mode of the column
    raw_data_df["Credit_History"]= raw_data_df["Credit_History"].fillna(raw_data_df["Credit_History"].mode()[0])
    
    #replace credit/noncredit values with 0/1
    has_credit = 0
    no_credit = 0

    for row in raw_data_df["Credit_History"]:
        if row == 1:
            has_credit += 1
        else:
            no_credit += 1        
    return raw_data_df

#Gender
def gender(data):
    # Find the mode of the gender data
    data['Gender'] = (data['Gender']
    .fillna(data['Gender'].mode()[0])
    )
    return data

#Married
def married(data):
    #missing values with mode
    data['Married'] = (data['Married']
    .fillna(data['Married'].mode()[0])
    )
    return data

#Education
def education(data):
    #missing values with mode
    data['Education'] = (data['Education']
    .fillna(data['Education'].mode()[0])
    )
    return data
#CoApplicant
def coapplicantIncome(data):
    #fill missing values with mean
    data['CoapplicantIncome'].fillna(
        data['CoapplicantIncome'].mean(), inplace=True
    )
    
    #Outliers
    Q1= data['CoapplicantIncome'].quantile(0.25) 
    Q3= data['CoapplicantIncome'].quantile(0.75)

    inter_quartile_range = Q3-Q1

    #find the inter quartile ranges
    lower_bound = Q1 - (1.5*inter_quartile_range)
    upper_bound = Q3 + (1.5*inter_quartile_range)
    #isolate outliers
    outliers_indexes = []
    for index, row in enumerate(data['CoapplicantIncome']):
        if row < lower_bound:
            outliers_indexes.append(index)
        else:
            if row > upper_bound:
                outliers_indexes.append(index)  
        # Reset index of the DataFrame
    data.reset_index(drop=True, inplace=True)
    #removing Outliers
    data.drop(outliers_indexes, inplace=True)
    
    return data

#Property Area
def property_area(data):
    #missing values with mode
    data['Property_Area'] = (data['Property_Area']
    .fillna(data['Property_Area'].mode()[0])
    )
    return data

#dependents
def dependants(data):
    data['Dependents'] = (data['Dependents']
    .fillna(data['Dependents'].mode()[0])
    )
    #print(data['Dependents'].unique())
    return data

#finally drop the first column for Applicant loan identification
def drop_id(data):
    data.drop('Loan_ID', axis = 1, inplace = True)
    return data

#call this function when we start preproccessing
def preproccessing():
    return (load_data()
            .pipe(loanAmount)
            .pipe(self_Employed)
            .pipe(loan_amount_term)
            .pipe(applicant_income)
            .pipe(Credit_History)
            .pipe(gender).pipe(married)
            .pipe(coapplicantIncome)
            .pipe(education)
            .pipe(dependants)
            .pipe(drop_id)
    )
    

def preproccessing_for_validation():
    return (load_data_for_validation()
            .pipe(loanAmount)
            .pipe(self_Employed)
            .pipe(loan_amount_term)
            .pipe(applicant_income)
            .pipe(Credit_History)
            .pipe(gender).pipe(married)
            .pipe(coapplicantIncome)
            .pipe(education)
            .pipe(dependants)
            .pipe(drop_id)
    )
data = preproccessing_for_validation()
#print(data.isnull().sum())

'''
 #remove outliers
     #find the quartile ranges to identify outliers
    Q1= data['Loan_Amount_Term'].quantile(0.25) 
    Q3= data['Loan_Amount_Term'].quantile(0.75)

    inter_quartile_range = Q3-Q1

    #isolate outliers
    # Find the interquartile ranges
    lower_bound = Q1 - (1.5 * inter_quartile_range)
    upper_bound = Q3 + (1.5 * inter_quartile_range)

    # Isolate outliers
    outliers_indexes = data[(data['Loan_Amount_Term'] < lower_bound) | (data['Loan_Amount_Term'] > upper_bound)].index

    # Removing outliers
    data = data.drop(outliers_indexes).reset_index(drop=True)
    #========================'''