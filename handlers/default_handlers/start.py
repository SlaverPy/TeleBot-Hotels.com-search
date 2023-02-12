from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['start, info'])
def bot_help(message: Message) -> None:
    """Функция для запуска бота:
    запускается, в случае, если пользователь выбрал команду /start, /info
    выводит сообщения приветствия и сообщает об ограничении поиска
    выводит доступные команды и их описание"""
    greeting_text = 'Привет! я бот для удобного поиска отелей,' \
                    'Внимание! Поиск по России в данный момент не работает ' \
                    'Для начала поиска воспользуйся одной и команд:'
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, greeting_text)
    bot.reply_to(message, '\n'.join(text))