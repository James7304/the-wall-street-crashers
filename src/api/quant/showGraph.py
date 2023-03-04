import matplotlib.pyplot as plt
import datetime

# Load the data from the file
with open('apple_values_by_day.csv', 'r') as f:
    lines = f.readlines()

# Parse the date and value data from the file
dates = []
values = []
for line in lines[1:]:
    date_str, value_str = line.strip().split(',')
    dates.append(datetime.datetime.strptime(date_str, '%Y-%m-%d').date())
    values.append(float(value_str))

# Create the plot
plt.plot(dates, values)

# Add titles and labels
plt.title('Apple Stock Prices by Day')
plt.xlabel('Date')
plt.ylabel('Price')

# Display the plot
plt.show()
