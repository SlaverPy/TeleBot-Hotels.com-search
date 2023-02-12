import datetime


def checking_the_date(first_day: datetime, second_day: str) -> datetime:
    """Функция для валидации даты
    Принимает 2 параметра:
    first_day - дата с которой будет проводится сравнение в формате datetime.date
    second_day - дата, для проверки в формате str
    проверяет строку на корректность ввода,
    возвращает сообщение с ошибкой или возвращает сформированную дату и вормате: datetime.date
    """
    try:
        if second_day[2] in ' .-':
            d, m, g = second_day.split(second_day[2])
            if len(d) > 2 or len(m) != 2 or len(g) != 4:
                raise ValueError
        else:
            raise ValueError
    except ValueError:
        return 'Указан неверный формат даты. Дата должна быть в формате "24-02-2022"'
    try:
        dt = datetime.date(int(g), int(m), int(d))
    except ValueError:
        return "такой даты не существует"
    if first_day >= dt:
        if first_day == datetime.date.today():
            return f'Дата въезда не может быть меньше или равна текущей даты'
        return f'Дата выезда не может быть меньше или равна даты въезда'
    return dt
