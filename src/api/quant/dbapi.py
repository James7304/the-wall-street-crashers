import pymysql.cursors

# # Set the database credentials
# host = "sql750.main-hosting.eu"
# user = "u202629177_wsc"
# password = "z0|xo@!K"
# database = "u202629177_wsc"
#
# # Create a connection to the database
# conn = pymysql.connect(
#     host=host,
#     user=user,
#     password=password,
#     database=database,
#     cursorclass=pymysql.cursors.DictCursor
# )
#
# # Create a cursor object to execute SQL queries
# cursor = conn.cursor()

class DBAPI:
    conn = None
    cursor = None
    @staticmethod
    def init():
        # Set the database credentials
        host = "sql750.main-hosting.eu"
        user = "u202629177_wsc"
        password = "z0|xo@!K"
        database = "u202629177_wsc"

        # Create a connection to the database
        DBAPI.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

        # Create a cursor object to execute SQL queries
        DBAPI.cursor = DBAPI.conn.cursor()
    @staticmethod
    def buy_stock(ticker, n, price):
        DBAPI.insert_stock(ticker, n, price)

        DBAPI.insert_trade(ticker, 'BUY', n, price)

        valuation = DBAPI.get_valuation()

    @staticmethod
    def sell_stock(ticker, n):
        price = DBAPI.get_stock(ticker)["price_per_unit"]
        DBAPI.drop_stock(ticker, n)

        DBAPI.insert_trade(ticker, 'SELL', n, price)

        valuation = DBAPI.get_valuation()

    @staticmethod
    def insert_stock(ticker, n, price):
        DBAPI.cursor.execute(f"insert into portfolio (ticker, quantity, price_per_unit) values ('{ticker}', {n}, {price})")
        DBAPI.conn.commit()

    @staticmethod
    def drop_stock(ticker, n):
        DBAPI.cursor.execute(f"select * from portfolio where ticker='{ticker}'")
        quantity = DBAPI.cursor.fetchone()["quantity"]
        DBAPI.cursor.execute(f"update portfolio set quantity={quantity-n} where ticker='{ticker}'")
        DBAPI.conn.commit()

        if quantity-n <= 0:
            DBAPI.cursor.execute(f"delete from portfolio where ticker='{ticker}'")
            DBAPI.conn.commit()
            return

    @staticmethod
    def insert_trade(ticker, type, quantity, price):
        trade_id = 0
        with open('last_trade_id.txt', "r+") as f:
            trade_id = int(f.read())
            trade_id += 1
            f.seek(0)
            f.write(str(trade_id))
            f.truncate()

        DBAPI.cursor.execute(f"insert into trades (trade_id, ticker, type, quantity, price) values ({trade_id}, "
                       f"'{ticker}', '{type}', {quantity}, {price})")
        DBAPI.conn.commit()

    @staticmethod
    def get_stock(ticker):
        DBAPI.cursor.execute(f"select * from portfolio where ticker='{ticker}'")
        return DBAPI.cursor.fetchone()

    @staticmethod
    def get_trade(trade_id):
        DBAPI.cursor.execute(f"select * from trades where trade_id={trade_id}")
        return DBAPI.cursor.fetchone()

    @staticmethod
    def get_trades(ticker):
        DBAPI.cursor.execute(f"select * from trades where ticker='{ticker}'")
        return DBAPI.cursor.fetchall()

    @staticmethod
    def get_valuation():
        DBAPI.cursor.execute("select * from portfolio")
        stocks = DBAPI.cursor.fetchall()
        return sum(stock["price_per_unit"] for stock in stocks)

    @staticmethod
    def clean_all():
        if input("Are you sure you want to clean the portfolio and trades tables ?").lower() != "y": return

        DBAPI.cursor.execute("delete from portfolio")
        DBAPI.conn.commit()

        DBAPI.cursor.execute("delete from trades")
        DBAPI.conn.commit()

    @staticmethod
    def close():
        DBAPI.cursor.close()
        DBAPI.conn.close()

# clean_all()
DBAPI.init()
print(DBAPI.get_trades("MSFT"))
DBAPI.close()