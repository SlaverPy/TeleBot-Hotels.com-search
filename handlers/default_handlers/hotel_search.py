import datetime

from telebot.types import Message, CallbackQuery, InputMediaPhoto

from config_data.config import MISTAKE, MISTAKE_HOTEL
from loader import bot

from keyboards.inline.choosing_city import choosing_a_city
from keyboards.inline.select_yes_no import select_yes_no
from keyboards.inline.quantity_photo import quantity_photo
from states.search_info import SearchInfoState

from functions.general_functions.collecting_information import getting_information_about_the_hotel
from functions.general_functions.date_validation import checking_the_date
from functions.general_functions.check_info import check_info

from functions.for_working_with_API.forming_querystring import forming_querystring

from database.sqlite_db import add_history
from config_data.config import logger


@bot.message_handler(commands=['lowprice', 'recommended', 'relevant'])
def starting_hotel_search(massage: Message) -> None:
    """функция для сбора основной информации:
    запускается, при введении пользователем команды
    начинает собирать информацию о городе : SearchInfoState.city"""
    logger.info(f'user_id={massage.from_user.id}, command={massage.text}')
    bot.set_state(massage.from_user.id, SearchInfoState.city, massage.chat.id)
    bot.send_message(massage.from_user.id, 'Для вывода интересующей вас информации мне понадобится кое-что уточнить:')
    bot.send_message(massage.from_user.id, 'Введите название города, в котором ищете отель')
    with bot.retrieve_data(massage.from_user.id, massage.chat.id) as data:
        data['command'] = massage.text


@logger.catch
@bot.message_handler(state=SearchInfoState.city)
def city_selection_buttons(massage: Message) -> None:
    """функция для сбора информации о городе:
    запускается, при отправки пользователем название города
    проверяет существование города
    выводит выбор кнопки с выбором города для пользователя"""
    city_search_list = choosing_a_city(massage.text)
    if len(city_search_list.keyboard):
        bot.send_message(massage.from_user.id, 'Уточните, пожалуйста:',
                         reply_markup=city_search_list)
    else:
        bot.send_message(massage.from_user.id, f'У меня нет информации о городе: {massage.text}')


@logger.catch
@bot.callback_query_handler(func=None, state=SearchInfoState.city)
def getting_the_selected_city(call: CallbackQuery) -> None:
    """Получает нажатую пользователем кнопку
    Запрашивает у пользователя дату въезда
    запускает состояние для записи даты въезда
    записывает id выбранного пользователем города
    Вызывает состояние записи даты въезда: SearchInfoState.date_of_entry"""
    for x in call.message.json['reply_markup']['inline_keyboard']:
        if call.data == x[0]['callback_data']:
            break
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, f"====Вы выбрали: {x[0]['text']}====")
    bot.send_message(call.from_user.id, 'введите дату въезда в формате(год-месяц-день): ДД ММ ГГГГ:')
    bot.set_state(call.from_user.id, SearchInfoState.date_of_entry, call.from_user.id)
    with bot.retrieve_data(call.from_user.id, call.from_user.id) as data:
        data['city'] = str(x[0]['callback_data'])
        data['city_name'] = x[0]['text']
        logger.info(f'user_id={call.from_user.id}, city={x[0]["text"]}')


@logger.catch
@bot.message_handler(state=SearchInfoState.date_of_entry)
def record_of_entry_date(massage: Message) -> None:
    """функция для сбора информации о дате въезда:
       запускается, при отправки пользователем даты
       сравнивает дату с текущей при помощи функции : date_vaid()
       начинает собирать информацию о дате выезда :  SearchInfoState.date_of_departure
       Записывает дату въезда"""
    today = datetime.date.today()
    verified_date = checking_the_date(today, massage.text)
    if isinstance(verified_date, datetime.date):
        bot.send_message(massage.from_user.id, 'На сколько ночей, планируете найти отель?')
        bot.set_state(massage.from_user.id, SearchInfoState.date_of_departure, massage.chat.id)
        with bot.retrieve_data(massage.from_user.id, massage.chat.id) as data:
            data['date_of_entry'] = verified_date
            data['ru_date_entry'] = massage.text
            logger.info(f'user_id={massage.from_user.id},date_entry={massage.text}')
    else:
        bot.send_message(massage.from_user.id, verified_date)


@logger.catch
@bot.message_handler(state=SearchInfoState.date_of_departure)
def record_of_departure_date(massage: Message) -> None:
    """функция для сбора информации о дате выезда:
       запускается, при отправки пользователем даты
       сравнивает дату с датой въезда при помощи функции : date_vaid()
       начинает собирать информацию о количестве отелей для выведения :  SearchInfoState.quantity
       записывает дату выезда"""
    if massage.text.isdigit():
        with bot.retrieve_data(massage.from_user.id, massage.chat.id) as data:
            entry_date = data["date_of_entry"]
            date_of_departure = entry_date + datetime.timedelta(days=int(massage.text))
            if data['command'] == '/relevant':
                    bot.send_message(massage.from_user.id, 'Укажите минимальную цену : $/сут')
                    bot.set_state(massage.from_user.id, SearchInfoState.price_min, massage.chat.id)
            else:
                bot.send_message(massage.from_user.id, 'Отлично, сколько отелей ты хотел бы увидеть?')
                bot.send_message(massage.from_user.id, ' Я могу вывести до 20 за раз! ')
                bot.set_state(massage.from_user.id, SearchInfoState.quantity, massage.chat.id)
            data['date_of_departure'] = date_of_departure
            data['ru_date_departure'] = datetime.date.strftime(date_of_departure, "%d-%m-%Y")
            logger.info(f'user_id={massage.from_user.id}, date_departure={massage.text}')

    else:
        bot.send_message(massage.from_user.id, 'Введите число')


@logger.catch
@bot.message_handler(state=SearchInfoState.quantity)
def get_quantity(massage: Message) -> None:
    """Функция для записи количества отелей, который желает запустить пользователь
    запускается при отправке пользователем количества отелей
    Проверяет что, пользователь запросил не более 20 отелей
    выводит кнопки,в которых запрашивает, хочет ли пользователь получить фото"""
    if int(massage.text) < 21:
        with bot.retrieve_data(massage.from_user.id, massage.chat.id) as data:
            data['quantity'] = massage.text
        bot.send_message(massage.from_user.id,
                         'Хотите ли вы получить фотографии отелей?',
                         reply_markup=select_yes_no())
        bot.set_state(massage.from_user.id, SearchInfoState.photo, massage.chat.id)
    else:
        bot.send_message(massage.from_user.id, 'Я могу вывести до 20 отелей за раз')


@logger.catch
@bot.callback_query_handler(func=None, state=SearchInfoState.photo)
def get_photo_question(call: CallbackQuery) -> None:
    """Функция для записи количества отелей, который желает запустить пользователь
    запускается при нажатии пользователем кнопки
    если пользователь нажал кнопку "Да":
        выводит кнопки для уточнения количества фотографий, которые он желает получить.
        запускает состояние 'photo_quantity'
    если пользователь нажал кнопку "Нет":
        Просит у пользователя проверить информацию
        выводит сообщение с параметрами поиска
        выводит кнопки для подтверждения
        запускает состояние 'final'
    """
    with bot.retrieve_data(call.message.chat.id) as data:
        if call.data == 'Yes':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.from_user.id,
                             'Сколько фотографий от каждого отеля вы хотите получить?',
                             reply_markup=quantity_photo())
            data['show_photo'] = call.data
            bot.set_state(call.from_user.id, SearchInfoState.photo_quantity, call.from_user.id)
        else:
            data['show_photo'] = 'No'
            data['photo_quantity'] = 0
            check_str = check_info(data)
            bot.send_message(call.from_user.id, "Проверьте информацию")
            bot.send_message(call.from_user.id, f"{check_str}\nВсе верно?", reply_markup=select_yes_no())
            bot.set_state(call.from_user.id, SearchInfoState.final, call.from_user.id)


@logger.catch
@bot.callback_query_handler(func=None, state=SearchInfoState.photo_quantity)
def get_photo_quantity(call: CallbackQuery) -> None:
    """Функция для записи количества фотографий для каждого отеля,
    запускается при нажатии пользователем кнопки
    записывает количество фотографий
    Просит у пользователя проверить информацию
    выводит сообщение с параметрами поиска
    выводит кнопки для подтверждения
    запускает состояние 'final''
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)
    with bot.retrieve_data(call.from_user.id) as data:
        data['photo_quantity'] = call.data
        check_str = check_info(data)
    bot.send_message(call.from_user.id, "Проверьте информацию")
    bot.send_message(call.from_user.id, f"{check_str}\nВсе верно?", reply_markup=select_yes_no())
    bot.set_state(call.from_user.id, SearchInfoState.final, call.from_user.id)


@logger.catch
@bot.callback_query_handler(func=None, state=SearchInfoState.final)
def issuing_information(call: CallbackQuery) -> None:
    """Функция для вывода отелей,
    запускается при нажатии пользователем кнопки
    если пользователь нажал кнопку "Да":
        выполняет запрос по введенным параметрам
        выводит
            информацию о каждом отеле
            сайт отеля
            фотографии, при необходимости
        либо
            информацию об ошибке
    если пользователь нажал кнопку "Нет":
        Сообщает что поиск прерван
        Удаляет состояние
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'No':
        bot.send_message(call.from_user.id, f'Поиск прерван')
        bot.delete_state(call.from_user.id)
    else:
        with bot.retrieve_data(call.from_user.id) as data:
            bot.send_message(call.from_user.id, f'Поиск информации...')
            result = forming_querystring(data)
            if isinstance(result, str):
                bot.send_message(call.from_user.id, MISTAKE)
            else:
                bot.send_message(call.from_user.id, f'-=Результат поиска по {data["city_name"]}=-')
                hotel_search = []
                count = 1
                for x in result['data']["propertySearch"]["propertySearchListings"]:
                    if x['__typename'] == "Property":
                        if str(bot.get_state(call.from_user.id)) != str(SearchInfoState.final):
                            break
                        try:
                            result = getting_information_about_the_hotel(x, int(data['photo_quantity']))
                            bot.send_message(call.from_user.id, f'{count}: ')
                            count += 1
                            if result[3]:
                                bot.send_message(call.from_user.id, 'Произошла ошибка ответа от сервера, часть данных не удалось получить: ')
                            bot.send_message(call.from_user.id, result[0])
                            logger.info(f'user_id={call.from_user.id}, search={result[0]}')
                            bot.send_message(call.from_user.id, f'[Сайт Отеля]({result[1]})', parse_mode='Markdown')
                            hotel_search.append(result[0].split('\n')[0].split(': ')[1])
                            image_list = []
                            if int(data['photo_quantity']) != 0:
                                for image in result[2]:
                                    image_list.append(InputMediaPhoto(image))
                                bot.send_media_group(call.from_user.id, media=image_list)
                        except Exception as ex:
                            logger.exception(ex)
                            bot.send_message(call.from_user.id, MISTAKE_HOTEL)
                add_history((call.from_user.id, data['command'], str(datetime.date.today()), ', '.join(hotel_search)))

