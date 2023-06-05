import cachetools
import psycopg2
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import dbname, user, password, host, port


class DataHandler:
    def __init__(self, bot):
        self.bot = bot
        self.current_page = 1
        self.cache = cachetools.LRUCache(maxsize=100)  # Создаем кэш размером до 100 элементов

    def get_data(self, page):
        if page in self.cache:
            return self.cache[page]  # Возвращаем данные из кэша, если они есть

        conn = psycopg2.connect(database=dbname, user=user, password=password, host=host,
                                port=port)
        cursor = conn.cursor()

        offset = (page - 1) * 3  # Количество строк для пропуска на основе номера страницы
        query = f"SELECT * FROM price_analysis WHERE price_difference_percent < 100 LIMIT 100 OFFSET {offset}"
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        self.cache[page] = data  # Сохраняем данные в кэше

        return data

    def generate_page_response(self, data):
        response = []
        for row in data:
            response.append([
                f"Symbol: {row[0]}",
                f"Exchanges: {', '.join(row[1])}",
                f"Min Price: {row[2]}",
                f"Max Price: {row[3]}",
                f"Price Difference: {format(row[4], '.8f')}",
                f"Price Difference Percent: {round(row[5], 2)}"
            ])
        return response

    def generate_inline_keyboard(self, current_page, total_pages):
        markup = InlineKeyboardMarkup()
        buttons_row = []

        if current_page > 1:
            prev_button = InlineKeyboardButton('<', callback_data='prev')
            buttons_row.append(prev_button)

        if current_page < total_pages:
            next_button = InlineKeyboardButton('>', callback_data='next')
            buttons_row.append(next_button)

        markup.row(*buttons_row)

        return markup

    def send_data_message(self, chat_id, response, page, total_pages, message_id=None):
        message = ''
        for row in response:
            message += '\n'.join(row) + '\n\n'

        markup = self.generate_inline_keyboard(page, total_pages)
        if message_id is None:
            self.bot.send_message(
                chat_id,
                f'Страница {page} из {total_pages}\n\n{message}',
                reply_markup=markup
            )
        else:
            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f'Страница {page} из {total_pages}\n\n{message}',
                reply_markup=markup
            )
