import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import joblib
import pickle

pd.set_option('display.max_columns', None)

# Load your trained machine learning model
model = joblib.load('./artifacts/model_b4_ft_eng.pk1')

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Loan Approval Prediction"),

    # Gender

    dcc.Dropdown(
        id='gender-dropdown',
        options=[
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'}
        ],
        value='',
        placeholder="Select Gender"
    ),

    # Married
    dcc.Dropdown(
        id='married-dropdown',
        options=[
            {'label': 'Married', 'value': 'Yes'},
            {'label': 'Not Married', 'value': 'No'}
        ],
        value='',
        placeholder="Select Marital Status"
    ),

    # Dependents
    dcc.Dropdown(
        id='dependents-dropdown',
        options=[
            {'label': '0 Dependents', 'value': 0},
            {'label': '1 Dependant', 'value': 1},
            {'label': '2 Dependant', 'value': 2},
            {'label': '+3 Dependant', 'value': 3}
        ],
        value='',
        placeholder="Select Amount of dependents"
    ),

    # Education
    dcc.Dropdown(
        id='education-dropdown',
        options=[
            {'label': 'I have a degree', 'value': 'Yes'},
            {'label': 'I do not have a degree', 'value': 'No'}
        ],
        value='',
        placeholder="Indication of degree"
    ),
    # Self_employed
    dcc.Dropdown(
        id='employment-dropdown',
        options=[
            {'label': 'Self employed', 'value': 'Yes'},
            {'label': 'Not self employed', 'value': 'No'}
        ],
        value='',
        placeholder="Indication of self employment"
    ),
    # Applicant_income
    dcc.Input(
        id='applicantIncome-input',
        type='number',
        value='',
        placeholder="Applicant Income Amount"
    ),
    # Coapplicant_income
    dcc.Input(
        id='coApplicantIncome-input',
        type='number',
        value='',
        placeholder="Co-Applicant Income Amount"
    ),
    # Loan_amount
    dcc.Input(
        id='loanAmount-input',
        type='number',
        value='',
        placeholder="Loan Amount"
    ),
    # Loan_term
    dcc.Input(
        id='loanTerm-input',
        type='number',
        value='',
        placeholder="Loan Term"
    ),
    # Credit_history
    dcc.Dropdown(
        id='creditHistory-input',
        options=[
            {'label': 'I have a credit history', 'value': 1},
            {'label': 'I do not have a credit history', 'value': 0},
        ],
        value='',
        placeholder="Indication of credit history"
    ),
    # Property_area
    dcc.Dropdown(
        id='property_area-input',
        options=[
            {'label': 'Urban', 'value': 2},
            {'label': 'Semiurban', 'value': 1},
            {'label': 'Rural', 'value': 0}
        ],
        value='',
        placeholder="Select Area you live in"
    ),

    # 'Gender': [gender],
    #     'Married': [married],
    #     'Dependents': [dependents],
    #     'Education': [education],
    #     'Self_Employed': [self_employed],
    #     'ApplicantIncome': [applicant_income],
    #     'CoapplicantIncome': [coapplicant_income],
    #     'LoanAmount': [loan_amount],
    #     'Loan_Amount_Term': [loan_term],
    #     'Credit_History': [credit_history],
    #     'Property_Area': [property_area]
    # Add other input components for Dependents, Education, Self_Employed, etc.
    
    html.Button('Predict Loan Approval', id='predict-button'),
    html.Div(id='prediction-output')
])

# Define callback to update prediction output
@app.callback(
    Output('prediction-output', 'children'),
    Input('predict-button', 'n_clicks'),
    State('gender-dropdown', 'value'),
    State('married-dropdown', 'value'),
    State('dependents-dropdown', 'value'),
    State('education-dropdown', 'value'),
    State('employment-dropdown', 'value'),
    State('applicantIncome-input', 'value'),
    State('coApplicantIncome-input', 'value'),
    State('loanAmount-input', 'value'),
    State('loanTerm-input', 'value'),
    State('creditHistory-input', 'value'),
    State('property_area-input', 'value'),
    # Add other input components as additional Input arguments
)

def update_prediction(n_clicks, gender, married, dependents, education, self_employed,
                      applicant_income, coapplicant_income, loan_amount,
                      loan_term, credit_history, property_area):
    if n_clicks == None:
        return ""
    
    # Fix input to correct type:
    list_binary = [gender, married, education, self_employed]
    list_new_values = []

    for val in list_binary:
        if val == 'Yes' or val == 'Male':
            list_new_values.append(1)
            list_new_values.append(0)
        else:
            list_new_values.append(0)
            list_new_values.append(1)
        




    # Create a DataFrame with user inputs
    user_data = pd.DataFrame({

        # Required columns:           

        # Gender
        'Gender_Male': [list_new_values[0]],
        'Gender_Female': [list_new_values[1]],

        # Married
        'Married_No': [list_new_values[3]],
        'Married_Yes': [list_new_values[2]],

        # Dependants
        'Dependents': [dependents],

        # Education
        'Education_Graduate': [list_new_values[4]],
        'Education_Not Graduate': [list_new_values[5]],

        # Self_employed
        'Self_Employed_No': [list_new_values[7]],
        'Self_Employed_Yes': [list_new_values[6]],

        # Applicant Income
        'ApplicantIncome': [applicant_income],

        # Coapplicant Income
        'CoapplicantIncome': [coapplicant_income],

        # Loan Amount
        'LoanAmount': [loan_amount],

        # Loan Amount Term
        'Loan_Amount_Term': [loan_term],

        # Credit History
        'Credit_History': [credit_history],

        # Property_Area
        'Property_Area': [property_area],

        # Total Income
        'TotalIncome': [(applicant_income + coapplicant_income)]
    
        
    })

    # print(user_data)

    # Make predictions using the trained model
    prediction = model.predict(user_data)[0]

    txt_color = 'black'

    if prediction == 1:
        result_text = "Congratulations! Your loan is approved."
        txt_color = 'green'
    else:
        result_text = "Sorry, your loan application is not approved."
        txt_color = 'red'

    return html.H3(result_text, style={'color': txt_color})

if __name__ == '__main__':
    app.run_server(debug=True)
