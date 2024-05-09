#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sn
from skimpy import clean_columns
import plotly.express as px

#load raw data
raw = pd.read_csv("././data/raw_data.csv")
meta = pd.read_csv("././Data/metadata.csv")
#isolate Coapplicant income table and Loan_Status
#Key details about given data
#-No missing null data
#data has over 300 duplicaate instances 
df = raw[['CoapplicantIncome']]
Co_applicant =raw[['CoapplicantIncome']]
test = df.select_dtypes("number").nunique()
#make column for box plot
column = ['CoapplicantIncome']

#Quartile and IQR
#find the quartile ranges to identify outliers
Q1= df['CoapplicantIncome'].quantile(0.25) 
Q2= df['CoapplicantIncome'].quantile(0.5)
Q3= df['CoapplicantIncome'].quantile(0.75)

inter_quartile_range = Q3-Q1

#find the inter quartile ranges
lower_bound = Q1 - (1.5*inter_quartile_range)
upper_bound = Q3 + (1.5*inter_quartile_range)

#isolate outliers
outliers_indexes = []
counter = 0
for index, row in enumerate(raw['CoapplicantIncome']):
    if row < lower_bound:
        outliers_indexes.append(index)
    else:
        if row > upper_bound:
            outliers_indexes.append(index)  

#Locate the outliers using the indexes from outliers_indexes
Outliers_df = raw['CoapplicantIncome'].loc[outliers_indexes]
#print(len(Outliers_df))
#print(Outliers_df.index)

#isolate outliers
Outliers_df = Co_applicant['CoapplicantIncome'].loc[outliers_indexes]

num_of_Outliers = len(outliers_indexes)
percentage_of_outliers = (num_of_Outliers)*100/len(df)
print(f"The percentage of outliers:\t{percentage_of_outliers.__round__(2)}%")

#Plot the box plot of the CoapplicantIncome column
pl.figure(figsize=(6,4))
sn.boxplot(x=raw['CoapplicantIncome'], color='skyblue')
sn.swarmplot(x=Outliers_df, color='red', label='Outliers')
pl.show() 

"""
- Oultiers account for only 2.93% of the data.
- These applicnats have acceptionally high Co-applicant iincomes 
- Due to them accountiong for such low pecetage of the data this may indicate tht the bank rarely come acc 
    applicants with such a high CAI "(Co applicant income)"
-and due to this these outliers will be removed 
"""

#removing Outliers
#Drop the whole rows with outliers was using inplace !(run once)
raw.drop(outliers_indexes, inplace=True)

#check the distribution of CoapplicantIncome:
pl.figure(figsize=(5, 5))
sn.histplot(Co_applicant, kde=True)
pl.title('Distribution of Co-applicant Income Before removing outliers')
pl.xlabel('Co-applican tIncome ')


pl.figure(figsize=(5, 5))
sn.histplot(Co_applicant['CoapplicantIncome'], kde=True)
pl.title('Distribution of Co-applicant Income after removing outliers')
pl.xlabel('Co-applicant-Income')
pl.show()

#Statistical measures

#Central Tendency
mean = raw['CoapplicantIncome'].mean().__round__(2)
median = raw['CoapplicantIncome'].median().__round__(2)

#Spread or Dispersion
std = raw['CoapplicantIncome'].std().__round__(2)
min = raw['CoapplicantIncome'].min().__round__(2)
max = raw['CoapplicantIncome'].max().__round__(2)

#Skewness
skew_coef =raw['CoapplicantIncome'].skew().__round__(2)
#K>0, heavier tails, K<0: lighter tails, k approx. 0: SIMILAR TAILS TO NORMAL
kurt_coeff = raw['CoapplicantIncome'].kurt().__round__(2)
 
print(f"Central Tendency:\n mean: {mean}\t median: {median}\n")
print(f"Spread:\n Standard deviation: {std}\t min:{min}\tmax:{max}\n")
print(f"Skewness coefficient: {skew_coef}\tKurtosis coefficent: {kurt_coeff}")

#Bivariate distributions

#Plot features to box plot that will repreaent the distribution of the data showing thr data range mean median and inter quatile range 
fig = px.box(data_frame=raw['CoapplicantIncome'], x='CoapplicantIncome', color=raw['Loan_Status'],
                 title=f'BoxPlot for Feature:CoapplicantIncome against the Target: Loan_Status')
fig.update_layout(xaxis_title=f'Loan_Status Feature')
fig.show()

"""
Observation form the data we can clearly tell that co applicnt income was not a decising factor 
in being awarded a Loan, from both box plots we a cettain that the lower 25% of applicants had no Co applicant 
income, further more the the avarage of those denied and those accepted had incomes of 268 and 1,239.5 along with an upper fence of 5701 for 'yes' Loae_Status  and 5302 for 'No' Loae_Status  
Key points
"""
# Log transformation
raw['Log_CoapplicantIncome'] = np.log(raw['CoapplicantIncome']) #created a new column
#print(raw_data_df.columns)

# Plot the transformed data
fig = px.histogram(data_frame=raw, x='Log_CoapplicantIncome', color='Loan_Status',
                   title='Histogram for Feature: LOG(LoanAmount) against the Target: Loan_Status',
                   facet_col='Loan_Status')
fig.update_layout(xaxis_title='Log(CoapplicantIncome) Feature', showlegend=False)
fig.show()

#Analysis
#To avoid scaling back using exp() well work with LoanAmount over log_LoanAmount
#Seperate column between yes and no
yes_df = raw[raw['Loan_Status'] == 'Y'][['CoapplicantIncome']]
no_df = raw[raw['CoapplicantIncome'] == 'N'][['CoapplicantIncome']]

#Stats

#mean
mean_yes = yes_df['CoapplicantIncome'].mean().__round__(2)
mean_no = no_df['CoapplicantIncome'].mean().__round__(2)

#standard deviation
std_yes = yes_df['CoapplicantIncome'].std().__round__(2)
std_no = no_df['CoapplicantIncome'].std().__round__(2)

#skewness
skew_yes = yes_df['CoapplicantIncome'].skew().__round__(2)
skew_no = no_df['CoapplicantIncome'].skew().__round__(2)

#min max
min_yes = yes_df['CoapplicantIncome'].min().__round__(2)
max_yes =yes_df['CoapplicantIncome'].max().__round__(2)
mode_yes =yes_df['CoapplicantIncome'].mode().__round__(2)
min_no = no_df['CoapplicantIncome'].min().__round__(2)
max_no =no_df['CoapplicantIncome'].max().__round__(2)

#print(yes_df.columns)
print(f"Total number:\n Yes: {len(yes_df)}\tNo: {len(no_df)}\n")
print(f"Range of Values:")
print(f"\tYes\n \tmin: {min_yes}\t max: {max_yes}\t mode: {mode_yes}")
print(f"\tNo\n min: {min_no}\t max: {max_no}")
print(f"The mean (average):\nYes: {mean_yes}\tNo: {mean_no}\n")
print(f"The Standard deviation (spread):\nYes: {std_yes}\tNo: {std_no}\n")
print(f"The skewness coeffcient:\nYes: {skew_yes}\tNo: {skew_no}\n")


#Pie chart that shows the approval rates of those with no Co-applicant invome versus those with co-applicant income
Appincome = raw[['CoapplicantIncome','Loan_Status']]
incom_positive = Appincome["CoapplicantIncome"]>0
print(Appincome[incom_positive])

Appincome = raw[['CoapplicantIncome','Loan_Status']]
incom_zero = Appincome["CoapplicantIncome"]==0
yes = Appincome[incom_positive]
no = Appincome[incom_zero]
#count values and calulate totals 
yes_total = yes['Loan_Status'].value_counts()
No_total= no['Loan_Status'].value_counts()
All_CoappIcY = yes_total['Y'] + yes_total['N']
All_CoappIcN = No_total['Y'] + No_total['N']
#calculating peercentages for approved loan applicatins for applicans with and without CoapplicantIncome
approved_with_CoAppInc = (yes_total['Y']/All_CoappIcY)*100
approved_without_CoAppInc = (No_total['Y']/All_CoappIcN)*100
#Create Pie charts and plot data
pl.figure(figsize=(3,3))
pl.pie(yes_total, labels= yes_total, colors=('#3361FF',"#FF33C4"))
pl.title("loan Approval rates with respect to applicanta having C applicant income")
pl.legend(labels=[f"\t\ napplicants approved with Co-applicant income: {yes_total['Y']}\n\
                applicants Declined with Co-applicant income: {yes_total['N']}\n\
                Total data entries: {All_CoappIcY}\n\
                Percatage of approved loans with Co-applicabt income: {approved_with_CoAppInc:.2f}%"
                
                ]
                    , loc='best', facecolor=None
                    )
pl.figure(figsize=(2,3))
pl.pie(No_total, labels= No_total, colors=('g',"r"))
pl.title("loan Approval rates with respect to applicanta having Co applicant income")
pl.legend(labels=[f"\t\
                applicants approved without Co-applicant income: {No_total['Y']}\n\
                applicants Declined without Co-applicant income: {No_total['N']}\n\
                Total data entries: {All_CoappIcN}\n\
                Percatage of approved loans without Co-applicabt income: {approved_without_CoAppInc:.2f}%"
                   
                   ]           
                    , loc='best', facecolor=None
                    )
pl.show()

"""
 from the pie charts we are able to deduce that over 70 percet of applicant had a higher achnce of getting
 a loan approved if they had Co--applicant income 
 """