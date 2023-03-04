import pymysql

# Set the database credentials
host = "sql750.main-hosting.eu"
user = "u202629177_wsc"
password = "z0|xo@!K"
database = "u202629177_wsc"

# Create a connection to the database
conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query to fetch all the data from the table
query = "SELECT * FROM users"
cursor.execute(query)

# Fetch all the data and print it to the screen
data = cursor.fetchall()
for row in data:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()