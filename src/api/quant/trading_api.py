from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

class TradingAPI:

    @staticmethod
    def init():
        with open("alpaca_trading_keys.txt") as f:
            lines = f.readlines()
            api = lines[0].replace("api: ", "").replace("\n", "")
            secret = lines[1].replace("secret: ", "").replace("\n", "")

        alpaca_trading_client = TradingClient("CKR5ZGXXOQGR2EACDKEY", "nLEFbNJRG4caZFmbLjrlCtdsdAoz1Ahc6fyHUsdF")
        alpaca_account = alpaca_trading_client.get_account()

        print(alpaca_account.account_blocked)
        print(alpaca_account.buying_power)

TradingAPI.init()