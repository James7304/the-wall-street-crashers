import yfinance as yf
import calendar

# Define the start and end dates for the data
start_date = '1985-01-01'
end_date = '2000-12-31'

# Open a file to write the results to
f = open('apple_values_by_month.csv', 'w')
f.write('Date, Value\n')

# Loop through each month and retrieve the opening value for that month
for year in range(1985, 2001):
    for month in range(1, 13):
        last_day = calendar.monthrange(year, month)[1]  # Calculate the last day of the month
        start_month = f"{year}-{month:02d}-01"
        end_month = f"{year}-{month:02d}-{last_day:02d}"

        # Retrieve the daily data for the specified month
        apple = yf.download('AAPL', start=start_month, end=end_month)

        # Check if the DataFrame is empty before trying to access its first row
        if len(apple) > 0:
            beginning_value = apple.iloc[0]['Open']
            f.write(f"{start_month}, {beginning_value}\n")

# Close the file
f.close()