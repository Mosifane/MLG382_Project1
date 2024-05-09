from sklearn.pipeline import make_pipeline # Model pipeline
from sklearn.metrics import accuracy_score #Metrices
from data_transformation import transformation
from sklearn.model_selection import train_test_split
import pandas as pd 
import plotly.express as px 
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.ensemble import RandomForestClassifier

def split_data(data_df):
    X = data_df.drop(columns=['Loan_Status'], inplace = False)
    Y = data_df['Loan_Status']

    #split data into training and testing 80/20
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


    # Base line model accuracy score
    acc_baseline = y_train.value_counts(normalize=True).max()
    print(f"Baseline Accuracy: {round(acc_baseline*100,2)}")
    return X_train, X_test, y_train, y_test

#RF hyper parameter tuning
def rf_hyperparam(X_train, X_test, y_train, y_test):
    n_estimators_range = [50,100,150,200]
    max_depths_range = range(1,16)
    
    training_acc = []
    validation_acc = []
    
    for n_estimators in n_estimators_range:
        for max_depth in max_depths_range:
            # Initialize Random Forest model with current hyperparameters
            rf_model = RandomForestClassifier(
                n_estimators=n_estimators, 
                max_depth=max_depth, random_state=42)
            
            rf_model.fit(X_train, y_train)
            
            training_acc.append(rf_model.score(X_train,y_train))
            validation_acc.append(rf_model.score(X_test,y_test))

    return n_estimators_range, max_depths_range, training_acc, validation_acc

#ploting accuracy scores
def plot_acc_score(n_estimators_range, max_depth_range, train_acc, val_acc):
    # Create a DataFrame to store these scores
    acc_data_df = pd.DataFrame({
        'n_estimators': np.repeat(n_estimators_range, len(max_depth_range)),
        'max_depth': list(max_depth_range) * len(n_estimators_range),
        'Training': train_acc,
        'Validation': val_acc
    })

    for n_estimator in n_estimators_range:
        df = acc_data_df[acc_data_df['n_estimators'] == n_estimator]
        
        fig = px.line(data_frame=df,
                      x='max_depth',
                      y=['Training', 'Validation'],
                      title=f'Training and Validation (Testing) accuracy scores for Random Forest (n_estimators={n_estimator})',
                      labels={'value': 'Accuracy', 'max_depth': 'Max Depth', 'variable': 'Dataset'},
                      color_discrete_sequence=['blue', 'red']
                      )
        fig.show()
        
    return

#train final model
def train_final_rf_model(X_train, X_test, y_train, y_test, n, depth):
    # Initialize Random Forest model with optimal hyperparameters
    rf_model = RandomForestClassifier(n_estimators=n, max_depth=depth, random_state=42)
    
    # Train the model
    rf_model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"The accuracy score is: {round(accuracy*100, 2)}% after feature training using the final Random Forest model.")
    
    # Save the model
    joblib.dump(rf_model, './artifacts/rf_model_ft_eng.pk2')
    
    return rf_model

def start_training():
    data_df = transformation()
    data_df['TotalIncome'] =  data_df['ApplicantIncome'] + data_df['CoapplicantIncome']
    
    
    #Replace loan amount with loan ratio
    data_df['LoanAmountRatio'] =  data_df['LoanAmount']/data_df['TotalIncome']
    
    
    #Loan Repayment capacity
    data_df['LoanRepaymentCap'] =  data_df['ApplicantIncome']/data_df['LoanAmount']
    
    #scale loan term period
    data_df['Loan_Amount_Term'] = np.log(data_df["Loan_Amount_Term"])
    
    #Drop to reduce redundancy: reduced accuracy score by 2%
    #data_df.drop(['ApplicantIncome', 'CoapplicantIncome'], axis=1, inplace=True)
    #data_df.drop(['LoanAmount'], axis=1, inplace=True)
    #data_df.drop(['Education_Graduate', 'Education_Not Graduate'], axis=1, inplace=True)
    
    X_train, X_test, y_train, y_test = split_data(data_df)
    (n_estimators_range, max_depths_range, 
    training_acc, validation_acc) = rf_hyperparam(X_train, X_test, y_train, y_test)
    
    plot_acc_score(n_estimators_range, max_depths_range, 
    training_acc, validation_acc)
    
    #n = 100 depth = 8 optimal from plots
    train_final_rf_model(X_train, X_test, y_train, y_test, 100, 8)
    
    return #data_df


#================uncomment functions one by one===================================

start_training()



