import joblib
import pandas as pd
from data_transformation import transformation_for_validation

#load the model
# Load the model
model = joblib.load('artifacts/rf_model_ft_eng.pk2')

# Extract features to ensure order
ft_names = model.feature_names_in_
val_data = transformation_for_validation()
val_data = val_data[ft_names]

predictions = model.predict(val_data)
print(predictions)








'''model = joblib.load('artifacts/model_b4_ft_eng.pk1')

#extract features to ensure order
ft_names = model.named_steps['decisiontreeclassifier'].feature_names_in_

val_data = transformation_for_validation()
val_data = val_data[ft_names]

predictions = model.predict(val_data)
print(predictions)'''

