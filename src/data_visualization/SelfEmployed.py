import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from LoanAmount import data_loanAmount

#load the data
data_df = data_loanAmount()
print(len(data_df))