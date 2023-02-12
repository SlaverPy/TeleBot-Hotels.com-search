from loader import bot
from states.search_info import SearchInfoState
from telebot.types import Message


@bot.message_handler(state=[SearchInfoState.city,
                            SearchInfoState.date_of_entry,
                            SearchInfoState.date_of_departure,
                            SearchInfoState.price_min,
                            SearchInfoState.price_max,
                            SearchInfoState.quantity,
                            SearchInfoState.photo,
                            SearchInfoState.photo_quantity,
                            SearchInfoState.final],
                     commands=['history', 'start', 'help'])
def cancel_scenario(message: Message) -> None:
    """Функция для сброса состояния поиска:
    запускается, если:
        пользователь выбрал команду /help, /history, /start
        в случае, если пользователь находится на стадии поиска отеля
    выводит сообщения об сбросе состояния и просит повторить команду
    """
    bot.send_message(message.from_user.id, 'Сбросили состояние')
    bot.send_message(message.from_user.id, 'Повторите команду')
    bot.delete_state(message.from_user.id)


@bot.message_handler(state=[SearchInfoState.city,
                            SearchInfoState.date_of_entry,
                            SearchInfoState.date_of_departure,
                            SearchInfoState.price_min,
                            SearchInfoState.price_max,
                            SearchInfoState.quantity,
                            SearchInfoState.photo,
                            SearchInfoState.photo_quantity,
                            SearchInfoState.final],
                     commands=['cancel'])
def cancel_scenario(message: Message) -> None:
    """Функция для сброса состояния поиска:
    запускается, если:
        пользователь выбрал команду /cancel
        в случае, если пользователь находится на стадии поиска отеля
    выводит сообщения об сбросе состояния поиска
    """
    bot.send_message(message.from_user.id, 'Сбросили состояние')
    bot.delete_state(message.from_user.id)