from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """Функция для вывода основных команд:
    запускается, в случае, если пользователь выбрал команду /help
    выводит сообщения об ограничении поиска
    выводит доступные команды и их описание"""
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, 'Внимание! Поиск по России в данный момент не работает ')
    bot.send_message(message.from_user.id, '\n'.join(text))

