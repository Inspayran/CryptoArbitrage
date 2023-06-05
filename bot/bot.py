import telebot

from bot.data_handler import DataHandler
from config import token


class CryptoArbitrageBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.user_data = {}

        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button = telebot.types.KeyboardButton('Получить данные')  # Кнопка "Получить данные"
            markup.add(button)
            user_id = message.chat.id
            self.user_data[user_id] = DataHandler(self.bot)
            self.bot.send_message(
                user_id,
                'Добро пожаловать! Нажмите кнопку "Получить данные", чтобы получить информацию о криптовалютах.',
                reply_markup=markup
            )

        # Обработчик кнопки "Получить данные"
        @self.bot.message_handler(func=lambda message: message.text == 'Получить данные')
        def get_data_handler(message):
            user_id = message.chat.id
            if user_id not in self.user_data:
                self.user_data[user_id] = DataHandler(self.bot)
            self.user_data[user_id].current_page = 1
            data = self.user_data[user_id].get_data(self.user_data[user_id].current_page)  # Получаем данные для текущей страницы
            response = self.user_data[user_id].generate_page_response(data)  # Генерируем ответ для сообщения
            total_pages = (len(data) + 2) // 3  # Общее количество страниц
            self.user_data[user_id].send_data_message(user_id, response[:3], self.user_data[user_id].current_page, total_pages)

        @self.bot.callback_query_handler(func=lambda call: True)
        def inline_button_handler(call):
            user_id = call.message.chat.id

            if call.data == 'prev':
                self.user_data[user_id].current_page -= 1  # Переход на предыдущую страницу
                if self.user_data[user_id].current_page < 1:
                    self.user_data[user_id].current_page = 1
            elif call.data == 'next':
                self.user_data[user_id].current_page += 1  # Переход на следующую страницу

            data = self.user_data[user_id].get_data(self.user_data[user_id].current_page)  # Получаем данные для текущей страницы
            response = self.user_data[user_id].generate_page_response(data)  # Генерируем ответ для сообщения

            total_pages = (len(data) + 2) // 3  # Общее количество страниц
            self.user_data[user_id].send_data_message(user_id, response[:3], self.user_data[user_id].current_page, total_pages,
                                                     call.message.message_id)  # Отправляем сообщение с обновленными данными

    def start(self):
        self.bot.polling()


if __name__ == '__main__':
    token = token
    bot = CryptoArbitrageBot(token)
    bot.start()
