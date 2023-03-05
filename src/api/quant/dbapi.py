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
    def __init__(self, type):
        # Set the database credentials
        host = "sql750.main-hosting.eu"
        user = "u202629177_wsc"
        password = "z0|xo@!K"
        database = "u202629177_wsc"

        self.type = type
        self.open()

    def buy_stock(self, ticker, n, price):
        self.insert_stock(ticker, n, price)
        self.insert_trade(ticker, 'BUY', n, price)
        self.valuation = self.get_valuation()

    def sell_stock(self, ticker, n):
        if ticker == "cash": return
        
        price = self.get_stock(ticker)["price_per_unit"]
        sold = self.drop_stock(ticker, n)
        self.insert_trade(ticker, 'SELL', sold, price)
        self.valuation = self.get_valuation()

    def insert_stock(self, ticker, n, price):

        self.cursor.execute(f"select * from {self.type}portfolio where ticker='{ticker}'")
        if len(self.cursor.fetchall()) >= 0:
            self.cursor.execute(f"update {self.type}portfolio set quantity=quantity+{n} , price_per_unit = {int(price * 100)} where ticker='{ticker}'")
            self.cursor.execute(f"update {self.type}portfolio set quantity=quantity-{n * int(price * 100)} where ticker='cash'")
            self.conn.commit()
            return

        self.cursor.execute(
            f"insert into {self.type}portfolio (ticker, quantity, price_per_unit) values ('{ticker}', {n}, {price})")
        self.conn.commit()

    def drop_stock(self, ticker, n):
        self.cursor.execute(f"select * from {self.type}portfolio where ticker='{ticker}'")
        result = self.cursor.fetchone()
        quantity = result["quantity"]
        price = result["price_per_unit"]
        self.cursor.execute(f"update {self.type}portfolio set quantity={quantity - n} where ticker='{ticker}'")
        self.conn.commit()

        numSold = n

        if quantity - n <= 0:
            self.cursor.execute(f"delete from {self.type}portfolio where ticker='{ticker}'")
            self.cursor.execute(f"udpate {self.type}portfolio set quantity=quantity+{quantity * price} where ticker='cash'")
            numSold = quantity

        self.cursor.execute(f"udpate {self.type}portfolio set quantity=quantity+{quantity * price} where ticker='cash'")
        self.conn.commit()
        
        return numSold

    def insert_trade(self, ticker, type, quantity, price):
        trade_id = 0
        with open('last_trade_id.txt', "r+") as f:
            trade_id = int(f.read())
            trade_id += 1
            f.seek(0)
            f.write(str(trade_id))
            f.truncate()

        self.cursor.execute(f"insert into {self.type}trades (trade_id, ticker, type, quantity, price) values ({trade_id}, "
                             f"'{ticker}', '{type}', {quantity}, {price})")
        self.conn.commit()

    def get_stock(self, ticker):
        self.cursor.execute(f"select * from {self.type}portfolio where ticker='{ticker}'")
        return self.cursor.fetchone()
    
    def get_stocks(self):
        self.cursor.execute(f"select * from {self.type}portfolio")
        return self.cursor.fetchall()

    def get_trade(self, trade_id):
        self.cursor.execute(f"select * from {self.type}trades where trade_id={trade_id}")
        return self.cursor.fetchone()

    def get_trades(self, ticker):
        self.cursor.execute(f"select * from {self.type}trades where ticker='{ticker}'")
        return self.cursor.fetchall()

    def get_valuation(self):
        self.cursor.execute(f"select * from {self.type}portfolio")
        stocks = self.cursor.fetchall()
        return sum(stock["price_per_unit"] for stock in stocks)

    def clean_all(self):
        if input("Are you sure you want to clean the portfolio and trades tables ?").lower() != "y": return

        self.cursor.execute(f"delete from {self.type}portfolio")
        self.conn.commit()

        self.cursor.execute(f"delete from {self.type}trades")
        self.conn.commit()


    def open():

        # Create a connection to the database
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

        # Create a cursor object to execute SQL queries
        self.cursor = self.conn.cursor()
        
    def close(self):
        self.cursor.close()
        self.conn.close()
