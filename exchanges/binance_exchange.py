from binance.spot import Spot


class BinanceAPI:
    def __init__(self):
        self.client = Spot()

    def get_crypto_prices(self):
        try:
            ticker_prices = self.client.ticker_price()
            crypto_prices = {}

            for ticker in ticker_prices:
                symbol = ticker['symbol']
                price = float(ticker['price'])
                crypto_prices[symbol] = price
            print('Данные успешно получены с биржи Binance.')
            return crypto_prices

        except Exception as e:
            raise ValueError(f"Ошибка при выполнении запроса: {str(e)}")

