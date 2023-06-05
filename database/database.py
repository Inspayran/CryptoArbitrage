import psycopg2


class DataBaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except psycopg2.Error as e:
            raise ValueError(f'Ошибка при подключении к базе данных: {str(e)}')

    def create_table(self, table_name):
        conn = self.connect()
        cursor = conn.cursor()

        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(20) NOT NULL,
            price NUMERIC(18, 8) NOT NULL
        );
        '''

        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def insert_crypto_prices(self, table_name, crypto_prices):
        conn = self.connect()
        cursor = conn.cursor()

        delete_query = f'''
            DELETE FROM {table_name}
        '''

        cursor.execute(delete_query)

        query = f'''
            INSERT INTO {table_name} (symbol, price)
            VALUES (%s, %s::NUMERIC)
        '''

        for symbol, price in crypto_prices.items():
            cursor.execute(query, (symbol, price))

        conn.commit()

        cursor.close()
        conn.close()

    def create_price_analysis_table(self, table_name):
        conn = self.connect()
        cursor = conn.cursor()

        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                symbol TEXT,
                exchanges TEXT[],
                min_price NUMERIC,
                max_price NUMERIC,
                price_difference NUMERIC(18, 8),
                price_difference_percent NUMERIC
            )
        '''

        cursor.execute(create_table_query)

        conn.commit()
        cursor.close()
        conn.close()

    def save_price_analysis_results(self, table_name, analyze_price_difference):
        conn = self.connect()
        cursor = conn.cursor()

        delete_query = f'''
            DELETE FROM {table_name}
        '''

        cursor.execute(delete_query)

        insert_query = f'''
            INSERT INTO {table_name} (
                symbol, exchanges, min_price, max_price, price_difference, price_difference_percent
            ) VALUES (%s, %s, %s, %s, %s, %s)
        '''
        for row in analyze_price_difference:
            symbol = row[0]
            exchanges = row[1]
            min_price = row[2]
            max_price = row[3]
            price_difference = format(row[4], ".8f")
            price_difference_percent = row[5]

            cursor.execute(insert_query, (symbol, exchanges, min_price, max_price,
                                          price_difference, price_difference_percent))

        conn.commit()
        cursor.close()
        conn.close()

