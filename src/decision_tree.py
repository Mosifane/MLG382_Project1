from sklearn.tree import DecisionTreeClassifier #Model
from sklearn.pipeline import make_pipeline # Model pipeline
from sklearn.tree import DecisionTreeClassifier #Model
from sklearn.metrics import accuracy_score #Metrices
from data_transformation import transformation
from sklearn.model_selection import train_test_split
import pandas as pd 
import plotly.express as px 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
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

def dec_Tree(X_train, X_test, y_train, y_test):
    depth_hyperparams = range(1,20)
    #hyperparameter tuning
    training_acc = [] #accuracy score during training of model
    validation_acc = [] #accuracy during testing of model
    
    #create a for loop to hold the scores 
    for depth in depth_hyperparams:
        
        model = make_pipeline(
            DecisionTreeClassifier(max_depth=depth, random_state=42)
        )
        
        #fit model
        model.fit(X_train, y_train)
        
        #calculate the accuracy scores and append
        training_acc.append(model.score(X_train, y_train))
        validation_acc.append(model.score(X_test, y_test))
    return depth_hyperparams, training_acc, validation_acc

def display_acc_scores(depth, train_acc, val_acc):
    #create a df to store these scores
    df = pd.DataFrame(
        data = {'Training': train_acc, 'Validation': val_acc},
        index=depth
    )
    #print(df)
    
    #graph plot
    fig = px.line(data_frame=df, x = depth, y = ['Training', 'Validation'],
                  title= 'Training and Validation (Testing) accuracy scores',
                  labels={'value': 'Accuracy', 'Depth': 'Tree Depth', 'variable': 'Dataset'})
    fig.show()
    return


def final_model(model_nr,depth, X_train, X_test, y_train, y_test):
    model_dt = make_pipeline(
        DecisionTreeClassifier(max_depth=depth, random_state=42)
    )
    
    model_dt.fit(X_train, y_train)
    y_pred_scores = model_dt.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred_scores)
    print(f"The accuracy score is: {round(accuracy*100,2)}% before feature engineering using decision tree")
    save_model(model_nr, model_dt)
    
    #print decision tree to show ft importance
    dt_plt(model_dt)
    return  model_dt

def save_model(which_model, model_dt):
    if which_model == 0:
        joblib.dump(model_dt, './artifacts/model_b4_ft_eng.pk1') 
        #print("Done saving model before ft engineering.")
    else:
        joblib.dump(model_dt, './artifacts/model_after_ft.pk22')
           
    return

#plot the tree
def dt_plt(final_model):
    ft_names = final_model.named_steps.decisiontreeclassifier.feature_names_in_
    plt.figure(figsize=(18,12))
    plot_tree(
        decision_tree=final_model.named_steps['decisiontreeclassifier'], 
        filled=True, 
        max_depth=4, 
        feature_names=ft_names, 
        class_names=True
    )
    plt.axis('off')
    plt.show()
    return

def start_training():
    data_df = transformation()
    data_df['TotalIncome'] =  data_df['ApplicantIncome'] + data_df['CoapplicantIncome']
   
    X_train, X_test, y_train, y_test = split_data(data_df)
    depth, train_acc, val_acc = dec_Tree(X_train, X_test, y_train, y_test)
    display_acc_scores(depth, train_acc, val_acc)
    
    #Evalueate the final model before ft. eng 
    final_depth = 3
    model_dt = final_model(0,final_depth, X_train, X_test, y_train, y_test)
    ft_importance(model_dt)
    return

#Extract and view important features
def ft_importance(model_dt):
    # Extract features and their coefficients
    coef = model_dt.named_steps["decisiontreeclassifier"].feature_importances_
    ft = model_dt.named_steps['decisiontreeclassifier'].feature_names_in_

    # Convert to Pandas Series
    ft_importance = pd.Series(
        np.exp(coef), index=ft
        ).sort_values(ascending=True)
    
    #Plot ft importance
    # Create horizontal bar chart of feature importances
    fig = px.bar(
        data_frame=ft_importance, 
        x=ft_importance[:16].values, 
        y=ft_importance[:16].index, 
        title="Feature Importance"
    )

    fig.update_layout(xaxis_title='Gini Importance', yaxis_title='')
    fig.show()
    return



#================uncomment function===================================

start_training()



