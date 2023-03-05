import pandas as pd
import tensorflow as tf

# Load the CSV file and convert the date column to datetime objects
df = pd.read_csv('new_data.csv', parse_dates=['Date'])

# Define the feature and target columns
feature_col = 'Date'
target_cols = ['Open', 'High', 'Low', 'Volume']

# Get the last row of the DataFrame to use as the input data for prediction
new_data = df.iloc[[-1]][feature_col]

# Load the saved model
model = tf.keras.models.load_model('stock_model.h5')

# Make a prediction on the new data
prediction = model.predict(new_data)

print(prediction)

#this thing doesn't work

