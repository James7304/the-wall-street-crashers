# IMPORT THE LIBRARY
import yfinance as yf
from datetime import datetime, timedelta

# CREATE TICKER INSTANCE FOR AMAZON
amzn = yf.Ticker("AMZN")

# DEFINE START AND END DATES
start_date = datetime(2000, 1, 1)
end_date = datetime(2010, 12, 31)

# DEFINE TIME DELTA FOR INTERVAL
interval = timedelta(days=6)

# OPEN CSV FILE FOR WRITING
with open('amazon_data.csv', 'w') as f:
    # WRITE HEADER TO CSV FILE
    f.write('Date, Open, High, Low, Close, Volume\n')

    # LOOP THROUGH 7-DAY PERIODS BETWEEN START AND END DATES
    date_range = start_date
    while date_range < end_date:
        # CALCULATE END DATE FOR INTERVAL
        interval_end = date_range + interval
        if interval_end > end_date:
            interval_end = end_date

        # RETRIEVE HISTORICAL DATA FOR AMAZON STOCK WITH 1-MINUTE INTERVALS
        amzn_hist = amzn.history(start=date_range.strftime('%Y-%m-%d'), end=interval_end.strftime('%Y-%m-%d'), interval='1d')

        # WRITE HISTORICAL DATA TO CSV FILE
        for index, row in amzn_hist.iterrows():
            print(date_range.strftime('%Y-%m-%d'))
            f.write(f"{index}, {row['Open']}, {row['High']}, {row['Low']}, {row['Close']}, {row['Volume']}\n")

        # UPDATE DATE RANGE FOR NEXT ITERATION
        date_range = interval_end

# PRINT MESSAGE WHEN FINISHED
print('Finished writing Amazon data to CSV file.')
