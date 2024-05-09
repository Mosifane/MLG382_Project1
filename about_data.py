#Aim: create a metadata.csv to better understand the data 
import pandas as pd
import numpy as np
#load the data and display the first 5 rows
raw_data = pd.read_csv("./data/raw_data.csv")
#print(raw_data.head(5))

#view the info() about the data
#raw_data.info()

#View statistical summaries of numeric data
#print(raw_data.describe())

#lets isolate missing values
missing_values = np.array( raw_data.isnull().sum().values)
#print(missing_values_totals)

metadata = pd.DataFrame({
    #note: missing values is already appended with
    #column names hence we dont add a column for column names.
    'missing Values': missing_values,
    'Data Type': raw_data.dtypes,
    'Description':['individual load id', 'Gender: Male or Female',
                   'Maritual status: No/Yes',
                   'Dependents: numeric has + next to the number for more than 3',
                   'Eduacation: Graduate/ Not Graduate',
                   'Self_Employes: Yes/No', 'Applicant income: positive whole numbers',
                   'CoApplicantIncome: Positive whole numbers',
                   'LoanAmount: positive whole number',
                   'Loan_Amount_Term: positive integer',
                   'Credit history: postive integer', 
                   'Property_Area: Urban, Semiurban, Rural',
                   'Loan_Status: Yes/No'
                   ]
}, index=None)
metadata.index = raw_data.columns #set the index of the metadata as the column names
metadata.index.name = 'Column Name' #sets name of the index
metadata.reset_index(inplace=True) 
#print(metadata.head(5))
#save metadata to csv
metadata.to_csv('./data/metadata.csv')
print(metadata.head())
