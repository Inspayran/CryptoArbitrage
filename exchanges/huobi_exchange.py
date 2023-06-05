import requests


class HuobiAPI:
    def __init__(self):
        self.base_url = 'https://api.huobi.pro'
        self.crypto_prices = {}

    def get_crypto_prices(self):
        url = f'{self.base_url}/market/tickers'

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                for item in data['data']:
                    symbol = item['symbol']
                    price = item['close']
                    self.crypto_prices[symbol.upper()] = price
                print('Данные успешно получены с биржи Huobi.')
                return self.crypto_prices
            else:
                raise ValueError("Не удалось получить данные о ценах криптовалют.")
        except requests.RequestException as e:
            raise ValueError(f"Ошибка при выполнении запроса: {str(e)}")

