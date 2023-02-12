from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def quantity_photo() -> InlineKeyboardMarkup:
    """Функция для вывода кнопок
    Создает кнопки с цифрами от 1 до 10
    Возвращает кнопки в одну линию
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('1', callback_data=1),
                 InlineKeyboardButton('2', callback_data=2),
                 InlineKeyboardButton('3', callback_data=3),
                 InlineKeyboardButton('4', callback_data=4),
                 InlineKeyboardButton('5', callback_data=5),
                 InlineKeyboardButton('6', callback_data=6),
                 InlineKeyboardButton('7', callback_data=7),
                 InlineKeyboardButton('8', callback_data=8),
                 InlineKeyboardButton('9', callback_data=9),
                 InlineKeyboardButton('10', callback_data=10)
                 )
    return keyboard