from loader import bot
from states.search_info import SearchInfoState
from telebot.types import Message, CallbackQuery


@bot.message_handler(state=SearchInfoState.price_min)
def get_price_min(massage: Message) -> None:
    """функция для записи минимальной цены поиска:
    запускается, в случае, если пользователь выбрал команду /bestdeal
    запрашивает у пользователя максимальную цену отеля
    запускает состояние SearchInfoState.price_max"""
    if massage.text.isdigit():

        bot.send_message(massage.from_user.id, 'Введите максимальную цену за ночь : $/сут')
        bot.set_state(massage.from_user.id, SearchInfoState.price_max, massage.chat.id)
        with bot.retrieve_data(massage.from_user.id, massage.chat.id) as data:
            data['price_min'] = massage.text
    else:
        bot.send_message(massage.from_user.id, "Введите число, например: 2500")



@bot.message_handler(state=SearchInfoState.price_max)
def get_price_max(massage : Message) -> None:
    """функция для записи максимальной цены поиска:
     запускается, после ввода минимально цены
     запрашивает у пользователя """
    if massage.text.isdigit():
        bot.send_message(massage.from_user.id, 'Отлично, сколько отелей ты хотел бы увидеть?')
        bot.send_message(massage.from_user.id, ' Я могу вывести до 20 за раз! ')
        bot.set_state(massage.from_user.id, SearchInfoState.quantity, massage.chat.id)
        with bot.retrieve_data(massage.from_user.id, massage.chat.id) as data:
            data['price_max'] = massage.text
    else:
        bot.send_message(massage.from_user.id, "Введите число, например: 2500")
