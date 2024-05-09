import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

def data_loanAmount():
    #load the data just move 1 folders out of current dir
    raw_data_df = pd.read_csv("././data/raw_data.csv")
   
    #fill missing values with mean
    raw_data_df['LoanAmount'].fillna(
        raw_data_df['LoanAmount'].mean()#, inplace=True
    )

    #find the quartile ranges to identify outliers
    Q1= raw_data_df['LoanAmount'].quantile(0.25) 
    Q2= raw_data_df['LoanAmount'].quantile(0.5)
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
    return self_Employed(raw_data_df)

def self_Employed(data_df):
    #fill missing values using mode of self employed
    data_df['Self_Employed'] = data_df['Self_Employed'].fillna(data_df['Self_Employed'].mode()[0])
    
    return data_df

