import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Load the data
raw_data = pd.read_csv("././data/raw_data.csv")

maritual_data = raw_data['Married']

# Find the mode of the gender data (assuming single mode)
mode = maritual_data.mode().values[0]
if mode == "Yes":
    mode = 1
elif mode == "No":
    mode = 0

# Encode genders (consider handling missing values if necessary)
le = LabelEncoder()
encoded_maritual = le.fit_transform(maritual_data)

# Replace all missing data with the mode of the data
encoded_maritual = np.where(encoded_maritual == 2, mode, encoded_maritual)

# Count the values in each gender category
a = np.array(encoded_maritual)
b = np.unique(a, return_counts=True)
yes_totals = b[1][1]
no_totals = b[1][0]
print(yes_totals)
print(no_totals)
maritual_totals = yes_totals, no_totals

# Calculate total entries with gender data
total_maritual_data = encoded_maritual.shape[0]

# Count occurrences for each combination of Married and Loan_Status
married_loan_counts = pd.crosstab(raw_data['Married'], raw_data['Loan_Status'])

married_loan_counts.plot(kind='bar', stacked=False, color= ['#A3F5F3', '#BB4DED'])
plt.xlabel('Married')
plt.ylabel('Count')
plt.title('Loan Status Distribution by Marital Status')

plt.legend(title='Loan Status')
plt.show()