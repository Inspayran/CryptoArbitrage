import requests


class OkxAPI:
    def __init__(self):
        self.base_url = 'https://www.okx.com/api/v5'
        self.crypto_prices = {}

    def get_crypto_prices(self):
        url = f'{self.base_url}/market/tickers'
        params = {
            'instType': 'SPOT',
        }

        try:
            response = requests.get(url, params)
            data = response.json()

            if response.status_code == 200 and 'data' in data:
                for item in data['data']:
                    symbol = item['instId'].replace('-', '')
                    price = item['last']
                    self.crypto_prices[symbol] = price
                print('Данные успешно получены с биржи OKX.')
                return self.crypto_prices
            else:
                raise ValueError("Не удалось получить данные о ценах криптовалют.")
        except requests.RequestException as e:
            raise ValueError(f"Ошибка при выполнении запроса: {str(e)}")

