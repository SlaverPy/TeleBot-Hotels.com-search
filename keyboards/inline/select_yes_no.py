from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_yes_no() ->InlineKeyboardMarkup:
    """Функция для вывода кнопок
    Создает кнопки с текстом Да, Нет
    Возвращает кнопки в одну линию
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Да', callback_data='Yes'),
                 InlineKeyboardButton('Нет', callback_data="No"))
    return keyboard