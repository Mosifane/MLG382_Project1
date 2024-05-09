import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Load the data
raw_data = pd.read_csv("./data/raw_data.csv")
meta = pd.read_csv('./data/metadata.csv')

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

# Prepare pie chart
plt.pie(gender_totals, labels=['Male', 'Female'], colors=['#A3F5F3', '#BB4DED'])
plt.title('Distribution of Genders')

# Create legend with information
legend_text = [
    f"Total number of Male: {gender_totals[0]}\n",
    f"Total number of Female: {gender_totals[1]}\n",
]
plt.legend(labels=legend_text, loc='upper right', facecolor=None)

plt.show()