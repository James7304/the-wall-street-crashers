import requests
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import datetime as dt
# Set API key and endpoint
api_key = '7KTQMHOTNVZNC39I'
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


# Remove missing values and outliers
df = df.dropna()
df = df[df['5. adjusted close'] > 0]


# Compute daily price change as percentage of previous day's close
df['price_change'] = (df['5. adjusted close'] - df['5. adjusted close'].shift(1)) / df['5. adjusted close'].shift(1)

#Remove NaN value introduced from above command 
df = df.dropna()

# Scale data to range between 0 and 1
scaler = MinMaxScaler()
df['price_change'] = scaler.fit_transform(df[['price_change']])

# Compute technical indicators
df['ma50'] = SMAIndicator(df['price_change'], window=50).sma_indicator()
df['ma200'] = SMAIndicator(df['price_change'], window=200).sma_indicator()
df['rsi14'] = RSIIndicator(df['5. adjusted close'], window=14).rsi()
df = df.dropna()

def average_directional_index(high, low, close, period):
    # Calculate directional movement 
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low 
    plus_dm = up_move.clip(lower=0)
    minus_dm = down_move.clip(lower=0)

    #Calculate True Range
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis = 1).max(axis=1, skipna=False)

    #Calculates the Directional Movement Index 
    tr_period = true_range.rolling(window=period).sum()
    plus_dm_period = plus_dm.rolling(window=period).sum()
    minus_dm_period = minus_dm.rolling(window=period).sum()
    plus_di = 100 * (plus_dm_period/tr_period)
    minus_di = 100 * (minus_dm_period/tr_period)
    dx = 100 * abs((plus_di - minus_di)/(plus_di + minus_di))

    #Calculates the ADX
    adx = dx.rolling(window=period).mean()

    return adx

df['adx14'] = average_directional_index(df['2. high'], df['3. low'], df['5. adjusted close'], 14)
df = df.dropna()

# Define features and target variable
X = df[['ma50', 'ma200', 'rsi14', 'adx14']]
y = df['price_change']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train random forest regression model
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)
"""
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
"""
# Evaluate model performance on testing data
mse = mean_squared_error(y_test, model.predict(X_test))
rmse = np.sqrt(mse)
print(f"RMSE on testing data: {rmse}")
print(df)
# Set start and end dates for prediction
start_date = dt.datetime(2022, 1, 1)
end_date = dt.datetime(2023, 3, 4)

# Create DataFrame for predictions
preds = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date, freq='D'), columns=['predicted_price_change'])
"""
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
"""