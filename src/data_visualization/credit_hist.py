import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from applicant_and_term import data_ApplicantTerm #for integration

raw_data_df = pd.read_csv("././data/raw_data.csv")

credit_history = raw_data_df["Credit_History"]

# replace empty rows with the mode of the column
credit_history=credit_history.fillna(raw_data_df["Credit_History"].mode()[0])

def univariate():
    has_credit = 0
    no_credit = 0

    for row in credit_history:
        if row == 1:
            has_credit += 1
        else:
            no_credit += 1

    x_axis = ["Has Credit History", "Has No Credit History"]
    y_axis = [has_credit, no_credit]

    plt.bar(x_axis, y_axis)
    plt.title("Credit History")
    plt.xlabel("Credit History")
    plt.ylabel("Number of people")
    plt.legend()
    plt.show()

def bivariate():
    columns = ["Credit_History", "Loan_Status"]
    df = raw_data_df[columns].dropna()

    with_credit_yes = 0
    with_credit_no = 0

    without_credit_yes = 0
    without_credit_no = 0

    for ndex, row in df.iterrows():
        if row["Credit_History"] == 1:
            if row["Loan_Status"] == "Y":
                with_credit_yes += 1
            else:
                with_credit_no += 1

        if row["Credit_History"] == 0:
            if row["Loan_Status"] == "Y":
                without_credit_yes += 1
            else:
                without_credit_no += 1

    yes_answers = [with_credit_yes, without_credit_yes]
    no_answers = [with_credit_no, without_credit_no]

    x_axis = np.arange(len(no_answers))
    width = 0.25

    plt.bar(x_axis, yes_answers,
            width=width, edgecolor='black',
            label='Loan was approved')
    plt.bar(x_axis + width, no_answers, color='g',
            width=width, edgecolor='black',
            label='Loan was denied')

    plt.xticks(x_axis + width/2, ['Credit_hist: 1', 'Credit_hist: 0'])
    plt.xlabel("Credit History")
    plt.ylabel("Number of people who applied")
    plt.title("Credit History vs Loan Status")
    plt.legend()
    plt.show()
    
#===============For integration =================================

def data_CredHist():
    raw_data_df = data_ApplicantTerm()
    
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
            
    return 

