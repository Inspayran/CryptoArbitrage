from datetime import datetime

from exchanges.binance_exchange import BinanceAPI
from exchanges.huobi_exchange import HuobiAPI
from exchanges.okx_exchange import OkxAPI
from database.arbitrage import Arbitrage


class Handler:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.binance_api = BinanceAPI()
        self.okx_api = OkxAPI()
        self.huobi_api = HuobiAPI()

        self.arbitrage = Arbitrage(self.db_manager)

        self.db_manager.create_table(table_name='binance')
        self.db_manager.create_table(table_name='okx')
        self.db_manager.create_table(table_name='huobi')
        self.db_manager.create_price_analysis_table(table_name='price_analysis')

    def handle(self):
        self.db_manager.insert_crypto_prices(table_name='binance', crypto_prices=self.binance_api.get_crypto_prices())
        self.db_manager.insert_crypto_prices(table_name='okx', crypto_prices=self.okx_api.get_crypto_prices())
        self.db_manager.insert_crypto_prices(table_name='huobi', crypto_prices=self.huobi_api.get_crypto_prices())
        self.db_manager.save_price_analysis_results(table_name='price_analysis',
                                                    analyze_price_difference=self.arbitrage.analyze_price_difference())
        print("Все данные были получены в:", datetime.now())

