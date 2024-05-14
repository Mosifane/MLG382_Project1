import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import joblib
import numpy as np
import plotly.express as px

pd.set_option('display.max_columns', None)

# Load your trained machine learning model
model = joblib.load('./artifacts/model_b4_ft_eng.pk1')

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
    return fig

# Create a Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout
app.layout = html.Div([
    dcc.Graph(figure=ft_importance(model)),
    html.H1("Loan Approval Prediction"),

    # Contains all the inputs
    html.Div([
        
        # Dropdowns
        html.Div([

            # Gender
            html.H3("Gender: *"),
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
            html.H3("Marital status: *"),
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
            html.H3("Dependants: *"),
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
            html.H3("Education: *"),
            dcc.Dropdown(
                id='education-dropdown',
                options=[
                    {'label': 'I have a degree', 'value': 'Yes'},
                    {'label': 'I do not have a degree', 'value': 'No'}
                ],
                value='',
                placeholder="Indication of degree"
            ),
        ], style={'width': '20%'}),

        # Sliders
        html.Div([
            # Applicant_income
            html.H3("Applicant Income:"),
            dcc.Slider(
                id='applicantIncome-input',
                min=0,
                max=11000,
                value=0,
                marks={
                    0: '0',
                    1000: '1000',
                    2000: '2000',
                    3000: '3000',
                    4000: '4000',
                    5000: '5000',
                    6000: '6000',
                    7000: '7000',
                    8000: '8000',
                    9000: '9000',
                    10000: '10000',
                    11000: '11000'
                },
                included=False
            ),
            # Coapplicant_income
            html.H3("Co-applicant Income:"),
            dcc.Slider(
                id='coApplicantIncome-input',
                min=0,
                max=11000,
                value=0,
                marks={
                    0: '0',
                    1000: '1000',
                    2000: '2000',
                    3000: '3000',
                    4000: '4000',
                    5000: '5000',
                    6000: '6000',
                    7000: '7000',
                    8000: '8000',
                    9000: '9000',
                    10000: '10000',
                    11000: '11000'
                },
                included=False
            ),
            # LoanAmount
            html.H3("Loan Amount:"),
            dcc.Slider(
                id='loanAmount-input',
                min=0,
                max=300,
                value=0,
                marks={
                    0: '0',
                    30: '30',
                    60: '60',
                    90: '90',
                    120: '120',
                    150: '150',
                    180: '180',
                    210: '210',
                    240: '240',
                    270: '270',
                    300: '300'
                },
                included=False
            ),
            # Loan_term
            html.H3("Loan Term:"),
            dcc.Slider(
                id='loanTerm-input',
                min=0,
                max=480,
                value=0,
                marks={
                    0: '0',
                    60: '60',
                    120: '120',
                    180: '180',
                    240: '240',
                    300: '300',
                    360: '360',
                    420: '420',
                    480: '480'
                },
                included=False
            ),
        ], style={'width': '40%'}),

        html.Div([
            # Self_employed
            html.H3("Employment: *"),
            dcc.Dropdown(
                id='employment-dropdown',
                options=[
                    {'label': 'Self employed', 'value': 'Yes'},
                    {'label': 'Not self employed', 'value': 'No'}
                ],
                value='',
                placeholder="Indication of self employment"
            ),
            # Credit_history
            html.H3("Credit History: *"),
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
            html.H3("Property Area: *"),
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

        ], style={'width': '20%'})

    ], style={'display': 'flex', 'gap': '3vw'}),

    html.Br(),
    html.Br(),

    # Contains the button and output.
    html.Div([
        html.Button('Predict Loan Approval', id='predict-button', style={'width': '30%', 'font-size': '2vw'}),

        html.Div([

            html.H5("Output: "),

            html.Div(id='prediction-output')

        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'gap': '2vw'})

    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'gap': '2vw', 'margin-bottom': '2vh'})

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

    if n_clicks == None or gender == None or married == None or dependents == None or education == None or self_employed == None or credit_history == None or property_area == None:
        return html.H1("Please enter the required values to get an output.")
    
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
        result_text = "You qualify for a loan."
        txt_color = 'green'
    else:
        result_text = "You do not qualify for a loan."
        txt_color = 'red'

    return html.H1(result_text, style={'color': txt_color})

# Run app server
if __name__ == '__main__':
    app.run_server(debug=True)
