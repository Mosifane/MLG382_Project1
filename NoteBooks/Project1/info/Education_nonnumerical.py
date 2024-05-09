import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

# Load the needed data from raw_data
raw_data = pd.read_csv('C:/Users/Kennedy/Documents/BelgiumCampus/school work/Third year/MGL382/Project1/data/raw_data.csv')
meta = pd.read_csv('C:/Users/Kennedy/Documents/BelgiumCampus/school work/Third year/MGL382/Project1/data/metadata.csv')

# Isolate the Education column and count the values in each category: Graduate and Not Graduate
Education_total = raw_data['Education'].value_counts()
missing_values_of_Education = meta.loc[meta['Column Name'] == 'Education', 'missing Values'].values[0]

# Calculate the percentage of missing values
total_education = raw_data['Education'].shape[0]
percentage_missing_data = (missing_values_of_Education / total_education) * 100

# NOw we get the percentages of which group got the loans and which ones didn't
Total_loan = raw_data['Loan_Status'].shape[0]

#Cheching the values of Education over the final amount of Loan_Status
graduate_approved = raw_data[(raw_data['Education'] == 'Graduate') & (raw_data['Loan_Status'] == 'Y')]

# Count the number of rows where Education is Graduate and Loan_Status is Y
graduate_approved_count = graduate_approved.shape[0]

# Filter rows where Education is Graduate and Loan_Status is N
graduate_denied = raw_data[(raw_data['Education'] == 'Graduate') & (raw_data['Loan_Status'] == 'N')]

# Count the number of rows where Education is Graduate and Loan_Status is N
graduate_denied_count = graduate_denied.shape[0]


#Now we redo the steps for when the edution is Not Gradute

#Cheching the values of Education over the final amount of Loan_Status
not_graduate_approved = raw_data[(raw_data['Education'] == 'Not Graduate') & (raw_data['Loan_Status'] == 'Y')]

# Count the number of rows where Education is Not Graduate and Loan_Status is Y
not_graduate_approved_count = not_graduate_approved.shape[0]

# Filter rows where Education is Not Graduate and Loan_Status is N
not_graduate_denied = raw_data[(raw_data['Education'] == 'Not Graduate') & (raw_data['Loan_Status'] == 'N')]

# Count the number of rows where Education is NOt Graduate and Loan_Status is N
not_graduate_denied_count = not_graduate_denied.shape[0]
'''print("Number of graduates with approved loans (Loan_Status = 'Y'): ", graduate_approved_count)
print("Number of graduates with denied loans (Loan_Status = 'N'): ", graduate_denied_count)
print("Number of not graduates with approved loans (Loan_Status = 'Y'): ", not_graduate_approved_count)
print("Number of not graduates with denied loans (Loan_Status = 'N'): ", not_graduate_denied_count)'''

# Display the values on the needed chart to show the data
plt.figure(figsize=(12, 12))
plt.pie([graduate_approved_count, graduate_denied_count, not_graduate_approved_count, not_graduate_denied_count], labels=['graduates_approved', 'graduates-denied', 'not graduate-approved', 'not graduate-denied'], colors=['#1F51FF', '#FF3131', '#ADD8E6', '#00FF00'], autopct='%1.1f%%')
plt.title('Distribution of Education Application')
plt.legend(labels=[f"Total number of Graduate who got the loan: {graduate_approved_count}",
                   f"Total number of Not Graduate who got the loan: {not_graduate_approved_count}",
                   f"Total number of Graduate who didn't get the loan: {graduate_denied_count}",
                   f"Total number of Not Graduate who didn't the loan: {not_graduate_denied_count}",
                   f"Total number of missing values: {missing_values_of_Education}",
                   f"The percentage of missing values is {percentage_missing_data:.2f}% "],
                   loc='upper right', facecolor=None)


# Data
education = ['Graduate', 'Not Graduate']
approved_counts = [graduate_approved_count, not_graduate_approved_count]
denied_counts = [graduate_denied_count, not_graduate_denied_count]

# Plotting
bar_width = 0.35
index = range(len(education))

fig, ax = plt.subplots()
bars1 = ax.bar(index, approved_counts, bar_width, label='Approved Loan')
bars2 = ax.bar([i + bar_width for i in index], denied_counts, bar_width, label='Denied')

# Adding labels, title, and legend
ax.set_xlabel('Education')
ax.set_ylabel('Count')
ax.set_title('Loan Status by Education')
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(education)
ax.legend()

plt.show()
