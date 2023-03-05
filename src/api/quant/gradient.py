import pandas as pd

# Read the data from the CSV file
data = pd.read_csv('.csv', parse_dates=['Date'], index_col=['Ticker', 'Date'])

# Create a new DataFrame to hold the results
results = pd.DataFrame(columns=['Ticker', 'Date', 'Average'])

# Loop over each group of data for each ticker
for ticker, group in data.groupby(level='Ticker'):
    # Calculate the difference between each pair of values and take the average
    diffs = group.diff().dropna()
    averages = (diffs['Open'] + diffs['Close']) / 2
    
    # Add the results to the new DataFrame
    results = results.append(pd.DataFrame({
        'Ticker': ticker,
        'Date': diffs.index[:-1],
        'Average': averages.values
    }), ignore_index=True)

# Write the results to a new CSV file
results.to_csv('averages.csv', index=False)