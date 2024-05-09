import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Load the data
raw_data = pd.read_csv("./data/raw_data.csv")

gender_data = raw_data['Gender']

# Find the mode of the gender data (assuming single mode)
mode = gender_data.mode().values[0]
if mode == "Male":
    mode = 0
elif mode == "Female":
    mode = 1
else: mode = 2

# Encode genders (consider handling missing values if necessary)
le = LabelEncoder()
encoded_gender = le.fit_transform(gender_data)

# Replace all missing data with the mode of the data
encoded_gender = np.where(encoded_gender == 2, mode, encoded_gender)

# Count the values in each gender category
a = np.array(encoded_gender)
b = np.unique(a, return_counts=True)
male_totals = b[1][1]
female_totals = b[1][0]
gender_totals = male_totals, female_totals

# Assuming 'Gender' and 'Loan_Status' columns exist in raw_data
gender_loan_counts = pd.crosstab(raw_data['Gender'], raw_data['Loan_Status'])

gender_loan_counts.plot(kind='bar', stacked=False, color= ['#A3F5F3', '#BB4DED'])
plt.xlabel('Gender')
plt.ylabel('Count')
plt.title('Loan Status Distribution by Gender')

plt.legend(title='Loan Status')
plt.show()