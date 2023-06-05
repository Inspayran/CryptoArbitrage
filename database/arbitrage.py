class Arbitrage:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def analyze_price_difference(self):
        conn = self.db_manager.connect()
        cursor = conn.cursor()

        query = '''
            SELECT 
                symbol, array_agg(DISTINCT exchange) AS exchanges,
                MIN(min_price) AS min_price,
                MAX(max_price) AS max_price,
                MAX(max_price) - MIN(min_price) AS price_difference,

                CASE
                    WHEN MIN(min_price) <> 0 THEN (MAX(max_price) - MIN(min_price)) / MIN(min_price) * 100
                    ELSE 0
                END AS price_difference_percent

            FROM (
                SELECT 
                    symbol, exchange,
                    MIN(price) AS min_price,
                    MAX(price) AS max_price
                FROM (
                    SELECT symbol, 'Binance' AS exchange, price FROM binance
                    UNION ALL
                    SELECT symbol, 'Okx' AS exchange, price FROM okx
                    UNION ALL
                    SELECT symbol, 'Huobi' AS exchange, price FROM huobi
                ) AS combined_data
                GROUP BY symbol, exchange
            ) AS aggregated_data

            GROUP BY symbol
            HAVING COUNT(DISTINCT exchange) > 1
            ORDER BY price_difference_percent DESC
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        print("Функция analyze_price_difference завершила свою работу успешно.")
        return rows
