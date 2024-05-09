# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from LoanAmount import data_loanAmount
import warnings
warnings.simplefilter('ignore', category=Warning, lineno=0, append=False)

#Add the missing values

def add_missing(data):

    # Replace the missing the data with the most frequent data in months
    frequentVal = data['Loan_Amount_Term'].mode().values[0]

    # Replace the NaN values with the frequent val:
    data['Loan_Amount_Term'].fillna(frequentVal, inplace=True)

    # Indicate change
    print("Missing Data:\n", data.isna().sum())

    # Display the number of Yes and No of the output feature
    if(data['Loan_Status'][0] == 'Y' or data['Loan_Status'][0] == 'N'):
        data['Loan_Status'] = data['Loan_Status'].map({'Y': 'Yes', 'N': 'No'})

    lb_items = data['Loan_Status'].value_counts()

    lb_items

    # Univariate
    fig = px.bar(
        data_frame=lb_items,
        x=lb_items.index,
        y=lb_items.values,
        title='Loan Status Imbalance',
        color=lb_items.index
    )

    fig.update_layout(xaxis_title='Status of loan', yaxis_title='Number of individuals')

    fig.show()

    # Plotting numeric features:
    
    fig = px.box(
        data_frame=data['ApplicantIncome'],
        x = data['ApplicantIncome'].values,
        title = f'BoxPlot for Applicant Income'
    )
        
    fig.update_layout(xaxis_title='Applicant Income', yaxis_title='Number of individuals')
    fig.show()

    fig = px.box(
        data_frame=data['ApplicantIncome'],
        x = data['ApplicantIncome'].values,
        color = data['Loan_Status'],
        title = f'BoxPlot for Applicant Income, where the feature is against the target'
    )
        
    fig.update_layout(xaxis_title='Applicant Income', yaxis_title='Number of individuals')
    fig.show()

    

    return data

def prep_data(data):
    # Remove outliers of ApplicantIncome
    Q1 = data['ApplicantIncome'].quantile(0.25)
    Q3 = data['ApplicantIncome'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_mask = (data['ApplicantIncome'] > lower_bound) & (data['ApplicantIncome'] < upper_bound)

    data = data[outlier_mask]

    return data

def displayGraph(data):
    # Display loan term in bar
    data['Loan_Amount_Term'].value_counts()

    fig = px.bar(
        data_frame=data,
        x=data['Loan_Amount_Term'].value_counts().index,
        y=data['Loan_Amount_Term'].value_counts().values,
        title='Timeframes given to individuals to pay their loans'
    )

    fig.update_layout(xaxis_title='Loan term in months', yaxis_title='Number of individuals')
    fig.show()

    # Display the term amount in a pie chart
    fig = px.pie(
        data_frame=data,
        values=data['Loan_Amount_Term'].value_counts().index,
        height=500,
        title='Timeframes given to individuals to pay their loan'
    )

    fig.show()

# Read file and add the data to the function
df = pd.read_csv('./data/raw_data.csv')

df1 = df[['Loan_ID', 'ApplicantIncome', 'Loan_Amount_Term', 'Loan_Status']]

df_add_missing = add_missing(df1)

df_preped_data = prep_data(df_add_missing)

displayGraph(df_preped_data)

# Create csv file
df_preped_data.to_csv('././data/preped_data.csv')

print(f"Prepared dataframe:\n", df_preped_data)



    
