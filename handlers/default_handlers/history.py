from telebot.types import Message

from database.sqlite_db import get_history
from loader import bot


@bot.message_handler(commands=['history'])
def get_hist(message: Message) -> None:
    """функция для вывода истории поиска:
    запускается, в случае, если пользователь выбрал команду /history
    выполнят запрос к функции 'get_history'
        передает в нее id пользователя

    выводит информацию из базы данных
    или сообщение об отсутствие записей"""
    history = get_history(message.from_user.id)
    send_mess = 'История ваших сообщений пустая.'
    if len(history) > 0:
        for one_history in history:
            send_mess = (f'Команда: {one_history[0]}'
                         f'\nДата запроса: {one_history[1]}'
                         f'\nСписок отелей: {one_history[2]}')
    bot.send_message(message.chat.id, send_mess)

