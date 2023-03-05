import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from datetime import timedelta

# Load the CSV file and convert the date column to datetime objects
df = pd.read_csv('new_data.csv', parse_dates=['Date'])

# Define the feature and target columns
feature_cols = ['Open', 'High', 'Low', 'Volume']
target_col = 'Close'

# Create a new column for the target value shifted one day forward
df['target'] = df[target_col].shift(-1)

# Drop the last row, which will have a NaN value in the 'target' column
df = df.drop(df.index[-1])

# Create a new column for the number of days between the current and target date
df['days'] = (df['Date'] - df['Date'].shift(-1)).dt.days

# Split the data into training and testing sets
train_data, test_data = train_test_split(df, test_size=0.2)

# Create the feature and target dataframes for the training set
X_train = train_data[feature_cols]
y_train = train_data['target']

# Create the feature and target dataframes for the testing set
X_test = test_data[feature_cols]
y_test = test_data['target']

# Build the neural network model
model = Sequential()
model.add(Dense(32, activation='relu', input_shape=(len(feature_cols),)))
model.add(Dense(1, activation='linear'))

# Compile the model with the mean squared error loss function and the Adam optimizer
model.compile(loss='mean_squared_error', optimizer=Adam())

# Train the model on the training data
model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)

# Evaluate the model on the testing data
loss = model.evaluate(X_test, y_test, verbose=0)
print(f'Testing loss: {loss}')

# Save the model to a file
model.save('stock_model.h5')
