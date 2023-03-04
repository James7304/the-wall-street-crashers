import requests
import pandas as pd

# Set API key and endpoint
api_key = 'YOUR_API_KEY'
endpoint = 'https://www.alphavantage.co/query'

# Define parameters for API call
params = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': 'AAPL',
    'outputsize': 'full',
    'apikey': api_key
}

# Make API call and store response as JSON
response = requests.get(endpoint, params=params)
data = response.json()

# Convert JSON to DataFrame
df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
df = df.astype(float)

import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Remove missing values and outliers
df = df.dropna()
df = df[df['5. adjusted close'] > 0]

# Compute daily price change as percentage of previous day's close
df['price_change'] = (df['5. adjusted close'] - df['5. adjusted close'].shift(1)) / df['5. adjusted close'].shift(1)

# Scale data to range between 0 and 1
scaler = MinMaxScaler()
df['price_change'] = scaler.fit_transform(df[['price_change']])

from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

# Compute technical indicators
df['ma50'] = SMAIndicator(df['price_change'], window=50).sma_indicator()
df['ma200'] = SMAIndicator(df['price_change'], window=200).sma_indicator()
df['rsi14'] = RSIIndicator(df['5. adjusted close'], window=14).rsi()
df['adx14'] = AverageTrueRange(df['2. high'], df['3. low'], df['5. adjusted close'], window=14).average_directional_index()

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Define features and target variable
X = df[['ma50', 'ma200', 'rsi14', 'adx14']]
y = df['price_change']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train random forest regression model
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Split data into training and testing sets
train_data = df.loc['2011-01-01':'2020-12-31']
test_data = df.loc['2021-01-01':'2021-12-31']

X_train = train_data[['ma50', 'ma200', 'rsi14', 'adx14']]
y_train = train_data['price_change']

X_test = test_data[['ma50', 'ma200', 'rsi14', 'adx14']]
y_test = test_data['price_change']

# Train random forest regression model on training data
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Evaluate model performance on testing data
mse = mean_squared_error(y_test, model.predict(X_test))
rmse = np.sqrt(mse)
print(f"RMSE on testing data: {rmse}")

import datetime as dt

# Set start and end dates for prediction
start_date = dt.datetime(2022, 1, 1)
end_date = dt.datetime(2023, 3, 4)

# Create DataFrame for predictions
preds = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date, freq='D'), columns=['predicted_price_change'])

# Make predictions for each day
for date in preds.index:
    # Get features for current day
    current_features = df.loc[date - pd.Timedelta(days=200):date - pd.Timedelta(days=1), ['ma50', 'ma200', 'rsi14', 'adx14']].tail(1)
    
    # Make prediction
    current_pred = model.predict(current_features)
    
    # Save prediction in DataFrame
    preds.loc[date] = current_pred[0]

# Only buy stocks if predicted price change is positive
bought_stocks = []
for date in preds.index:
    if preds.loc[date, 'predicted_price_change'] > 0:
        bought_stocks.append(date)
