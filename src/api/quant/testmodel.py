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
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from dbapi import DBAPI
import atexit

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
    # with open("temp.txt", "w+") as f:
#     f.write(df["price_change"].to_string())
    adx = dx.rolling(window=period).mean()

    return adx

def define_df(ticker):    
    # Set API key and endpoint
    api_key = '7KTQMHOTNVZNC39I'
    endpoint = 'https://www.alphavantage.co/query'

    # Define parameters for API call
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': ticker,
        'outputsize': 'full',
        'apikey': api_key
    }

    # Make API call and store response as JSON
    # response = requests.get(endpoint, params=params)
    # data = response.json()

    df = yf.download(ticker, start="1990-01-01", end="2023-03-05")
    #df = df.iloc[::-1]
    df.index = df.index.date.astype(str)
    df = df.rename(columns={"Open": "1. open", "High": "2. high", "Low": "3. low", "Close": "4. close", "Adj Close": "5. adjusted close", "Volume": "6. volume", "Dividends": "7. dividend amount", "Stock Splits": "8. split coefficient"})
    df = df.astype(float)
    df["7. dividend amount"] = np.array(0)
    df["8. split coefficient"] = np.array(1.0)
    # print(df_tickers)
    # Convert JSON to DataFrame

    # df = df_tickers
    # df = df.astype(float)

    # sns.lineplot(x=df.loc["2021-01-01":"2020-01-01",].index, y="4. close", data=df.loc["2021-01-01":"2020-01-01",])
    # # plt.plot(df.loc["2021-01-01":"2020-01-01", "4. close"])
    # plt.show()
    shape_before = df.shape
    with open("temp.txt", "w+") as f:
        f.write(df.to_string())

    # df = pd.concat([df, df], axis=0)
    
    # Remove missing values and outliers
    df = df.dropna()
    df = df[df['5. adjusted close'] > 0]

    
    # Compute daily price change as percentage of previous day's close
    df['price_change'] = (df['5. adjusted close'] - df['5. adjusted close'].shift(1)) / df['5. adjusted close'].shift(1)

    #Remove NaN value introduced from above command 
    #df = df.dropna()
    
    # Scale data to range between 0 and 1
    # scaler = MinMaxScaler()
    # df['price_change'] = scaler.fit_transform(df[['price_change']])

    # Compute technical indicators
    df['ma50'] = SMAIndicator(df['price_change'], window=50).sma_indicator()
    df['ma200'] = SMAIndicator(df['price_change'], window=200).sma_indicator()
    df['rsi14'] = RSIIndicator(df['5. adjusted close'], window=14 ).rsi()
    # df = df.dropna()
    
    # print(df[df.isna().any(axis=1)])
    
    df['adx14'] = average_directional_index(df['2. high'], df['3. low'], df['5. adjusted close'], 14)
    df = df.dropna()
    
    shape_after = df.shape
    print("Shape before: " + str(shape_before[0]) + ", shape after: " + str(shape_after[0]))
    #print("IsNa:")
    #print(df)

    # Define features and target variable
    X = df[['ma50', 'ma200', 'rsi14', 'adx14']]
    y = df['price_change']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train random forest regression model
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model performance on testing data
    mse = mean_squared_error(y_test, model.predict(X_test))
    rmse = np.sqrt(mse)
    print(f"RMSE on testing data: {rmse}")

    return (model, df)

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


# Set start and end dates for prediction
start_date = dt.datetime(2022, 1, 1).date()
end_date = dt.datetime(2023, 3, 4).date()

# Create DataFrame for predictions
#preds = pd.DataFrame(index=df.index, columns=['predicted_price_change'])
#print(preds)

# preds.index.apply(lambda x: pd.Timestamp(x))
# Make predictions for each day
# df.index.values.astype(str)
# print(df)

# date = pd.Timestamp("2023-03-01")
# print(str(date - pd.Timedelta(days=200))[:10])
# print(str(date - pd.Timedelta(days=200))[:10], str(date - pd.Timedelta(days=1))[:10],)

# print(df.loc[str(date - pd.Timedelta(days=1))[:10]:str(date - pd.Timedelta(days=200))[:10], cols])

def predicted_price_change(ticker, df, model, date):
    # global cols
    cols = ['ma50', 'ma200', 'rsi14', 'adx14']
    # date = pd.Timestamp(df.index[0])
    # date = pd.Timestamp("2023-03-15")
    #lookahead_date = date + pd.Timedelta(lookahead_days)
    #lookahead_date = pd.Timestamp("2023-03-05")
    end_date = str(date - pd.Timedelta(days=1))[:10]
    start_date = str(date - pd.Timedelta(days=200))[:10]

    current_features = df.loc[start_date:end_date, cols].tail(1)
    # print(df.loc[str(date - pd.Timedelta(days=1)):str(date - pd.Timedelta(days=200)), cols])
    #future_features = df.loc[str(lookahead_date - pd.Timedelta(days=1)):str(lookahead_date - pd.Timedelta(days=200)), cols].tail(1)

    return model.predict(current_features)

# with open("temp.txt", "w+") as f:
#     f.write(df["price_change"].to_string())

# price_change = [predicted_price_change("", df, pd.Timestamp("2023-02-04") + pd.Timedelta(days=i)) for i in range(100)]
# df.loc["2023-03-03":"2023-02-03", "price_change"].plot()
# plt.show()

# mse2 = mean_squared_error(df["price_change"].head(100).values, price_change)
# print("RMSE2: " + str(np.sqrt(mse2)))


balance_over_time = []
def trialRun(tickers, start_date, end_date):
    global balance_over_time
    initialBalance = 5000
    # for date in dates:
    #     predictions = [(tuple[2], predicted_price_change("", tuple[1], tuple[0] pd.Timestamp(date))) for tuple in data]
    #     max = max([prediction[1] for prediction in predictions])

    #     max = (data[0][2], predicted_price_change("", data[0][1], data[0][0] pd.Timestamp(date)))
    #     for tuple in data:
    #         if predicted_price_change("", data[0][1], data[0][0] pd.Timestamp(date)) > max[1]:
    #             max = (tuple[2], predicted_price_change("", tuple[1], tuple[0] pd.Timestamp(date)))

        
    #     initialBalance *=  1 + ((df.loc[str(date)[:10], "4. close"] - df.loc[str(date)[:10], "1. open"]) / df.loc[str(date)[:10], "1. open"])
    #     balance_over_time.append((date, initialBalance))


        # for tuple in data:
        #     model = tuple[0]
        #     df = tuple[1]
        #     if predicted_price_change("", df, model, pd.Timestamp(date)) > 0:
        #         initialBalance *=  1 + ((df.loc[str(date)[:10], "4. close"] - df.loc[str(date)[:10], "1. open"]) / df.loc[str(date)[:10], "1. open"])
        #         balance_over_time.append((date, initialBalance))

    ticker_data = {}
    for ticker in tickers:
        ticker_data[ticker] = define_df(ticker)

    # dates = [ticker_data[ticker][1].loc[end_date:start_date,].index.values.tolist() for ticker in ticker_data.keys()]
    # dates = set(dates[0]).intersection(*dates)


    date = start_date
    # for date in dates:
    while date <= end_date:
        ticker_investment = predict_today(tickers, initialBalance, date)
        
        ticker_prediction_data = {}
        for ticker in ticker_data.keys():
           model = ticker_data[ticker][0]
           df = ticker_data[ticker][1]
           ticker_prediction_data[ticker] = predicted_price_change("", df, model, pd.Timestamp(date))

        #max_ticker = min(ticker_prediction_data, key=lambda x:ticker_prediction_data[x])
        #if ticker_prediction_data[max_ticker] < 0:
        for ticker in ticker_investment.keys():
            initialBalance +=  ticker_investment[ticker] * ((ticker_data[ticker][1].loc[str(date)[:10], "4. close"] - ticker_data[ticker][1].loc[str(date)[:10], "1. open"]) / ticker_data[ticker][1].loc[str(date)[:10], "1. open"])
            balance_over_time.append((date, initialBalance))
        
        date += pd.Timedelta(days=1)

    return initialBalance

def predict_today(tickers, investment, date):
    ticker_data = {}
    for ticker in tickers:
        ticker_data[ticker] = define_df(ticker)

    ticker_prediction_data = {}
    for ticker in ticker_data.keys():
        model = ticker_data[ticker][0]
        df = ticker_data[ticker][1]
        pred = predicted_price_change("", df, model, pd.Timestamp(date))
        if pred < 0:
            ticker_prediction_data[ticker] = (pred, df.loc[df.index.values[-1], "4. close"])

    total_pred = sum([pred[0] for pred in ticker_prediction_data.values()])
    ticker_investment = {}
    for ticker in ticker_prediction_data.keys():
        ticker_investment[ticker] = (((investment * ticker_prediction_data[ticker][0] / total_pred) / ticker_prediction_data[ticker][1])[0], ticker_prediction_data[ticker][1])
    print(ticker_investment)
    return ticker_investment
        
        


# model_aapl, df_aapl = define_df("AAPL")



# plt.plot(balance_over_time)
# plt.plot(df.loc["2023-01-02":"2021-12-06", "4. close"])
# plt.show()


model_aapl, df_aapl = define_df("NEX.L")
# model_meta, df_meta = define_df("META")
# model_nflx, df_nflx = define_df("NFLX")
# model_tsla, df_tsla = define_df("TSLA")
# model_msft, df_msft = define_df("MSFT")

# print(df_aapl)
indices = df_aapl.loc["2010-03-07":"2008-01-01", "price_change"].index.values
start_date = pd.Timestamp("2020-01-01")
end_date = pd.Timestamp("2023-03-05")
# print(indices)
# (model_aapl, df_aapl, "AAPL"), (model_meta, df_meta, "META"), (model_nflx, df_nflx, "NFLX"), (model_tsla, df_tsla, "TSLA"), (model_msft, df_msft, "MSFT")
tickers = ["AAPL", "NFLX", "MSFT", "META", "AMZN", "TSLA"]
#print(predict_today(tickers, 5000))
# print(trialRun(tickers, start_date, end_date))
"""
for date in preds.index:
    # Get features for current day
    #date = pd.Timestamp(date.date())
    current_features = df.loc[str(date)[:10], ['ma50', 'ma200', 'rsi14', 'adx14']]
    #current_features = df.loc[date - pd.Timedelta(days=200):date - pd.Timedelta(days=1), ['ma50', 'ma200', 'rsi14', 'adx14']]
    print(current_features)
    
    # Make prediction
    current_pred = model.predict(current_features)

    # Save prediction in DataFrame
    preds.loc[date] = current_pred[0]
    

"""
"""
# Only buy stocks if predicted price change is positive
bought_stocks = []
for date in preds.index:
    if preds.loc[date, 'predicted_price_change'] > 0:
        bought_stocks.append(date)
"""

#print(predicted_price_change("something", "2023-02-25", df))

all_allowed_stocks = ["AAPL", "MSFT", "TSLA", "NFLX", "META"]#, "GOOG", "NVDA", "ABNB", "PANW", "ZM", "CRWD"]
dbapi = DBAPI("alpha_")
atexit.register(dbapi.close)

portfolio = []

cash = 50000
valuation = cash
def daily_update(date):
    global valuation
    global cash

    owned_stocks = dbapi.get_stocks()
    # print(owned_stocks)
    try:
        for stock in owned_stocks:
            dbapi.sell_stock(stock["ticker"], stock["quantity"])
            # cash += stock["quantity"] * stock["price_per_unit"]
            # dbapi.log_balance(float(dbapi.get_valuation()) / 100, str(date))
    except Exception as e:
        print(e)

    print("valuation after selling: " + str(float(dbapi.get_valuation()) / 100))
    preds = predict_today(all_allowed_stocks, float(dbapi.get_valuation()) / 100, date)

    for ticker in preds.keys():
        dbapi.buy_stock(ticker, preds[ticker][0], preds[ticker][1])

        # cash -= preds[ticker][0] * preds[ticker][1]

        # dbapi.log_balance(float(dbapi.get_valuation()) / 100, date.strftime('%Y-%m-%d %H:%M:%S'))
        # dbapi.log_balance(float(dbapi.get_valuation()) / 100, str(date))
    dbapi.log_balance(float(dbapi.get_valuation()) / 100, date.strftime('%Y-%m-%d %H:%M:%S'))

start_date = pd.Timestamp("2020-01-01")
end_date = pd.Timestamp("2020-12-31")
date = start_date
while date <= end_date:
    daily_update(date)

    date += pd.Timedelta(days=30)

print(dbapi.get_valuation())

dbapi.close()