from telebot.handler_backends import State, StatesGroup


class SearchInfoState(StatesGroup):
    """Класс SearchInfoState
    Наследуется от StatesGroup
    -----------------------

    Определяет текущее состояние поиска

        city = 'Поиск города'
        date_of_entry = 'Запись даты въезда'
        date_of_departure = 'Запись даты выезда'
        price_min = 'Запись минимальной цены'
        price_max = 'Запись максимальной цены'
        quantity = 'Количество отелей для вывода'
        photo = 'Выводить ли фото'
        photo_quantity = 'Количество фото для вывода'
        final = 'Вывод отелей на основе собранной информации'
    """
    city = State()
    date_of_entry = State()
    date_of_departure = State()
    price_min = State()
    price_max = State()
    quantity = State()
    photo = State()
    photo_quantity = State()
    final = State()
