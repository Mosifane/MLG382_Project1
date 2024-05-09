import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Load the data
raw_data = pd.read_csv("./data/raw_data.csv")
meta = pd.read_csv('./data/metadata.csv')
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
maritual_totals = yes_totals, no_totals

# Prepare pie chart
plt.figure(figsize=(8, 8))
plt.pie(maritual_totals, labels=['Married', 'Unmarried'], colors=['#A3F5F3', '#BB4DED'])
plt.title('Distribution of Marital Status')

# Create legend with information
legend_text = [
    f"Number of married people: {maritual_totals[0]}\n",
    f"Number of unmarried people: {maritual_totals[1]}\n",
]
plt.legend(labels=legend_text, loc='upper right', facecolor=None)
plt.show()