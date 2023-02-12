import os
import sqlite3

path = os.path.abspath(os.path.join('database', 'search_history.sqlite'))


def create_db() -> None:
    """Функция для создании базы данных sqlite3"""
    db = sqlite3.connect(path)
    query = db.cursor()
    query.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER NOT NULL,
        command VARCHAR(255),
        date VARCHAR(255),
        hotels VARCHAR(255)

    )""")
    db.commit()


def add_history(history: tuple) -> None:
    """Добавляет в базу данный запись:
    Проверяет существует ли база данных
        если нет, вызывает функцию для её создания
    user_id : айди пользователя
    command : команда введенная пользователем
    date : даты запроса
    hotels : список полученных отелей"""
    if not os.path.exists('search_history.sqlite'):
        create_db()
    with sqlite3.connect(path) as con:
        query = con.cursor()
        query.execute("""INSERT INTO users (user_id, command, date, hotels)
            VALUES(?, ?, ?, ?);""", history)
        con.commit()


def get_history(user_id: int) -> list:
    """Получает запись из базы данных:
    Проверяет существует ли база данных
        если нет, вызывает функцию для её создания
    получает последние 10 записей из базы данных
    соответствующие ади пользователя
    возвращает список с записями"""
    if not os.path.exists('search_history.sqlite'):
        create_db()
    with sqlite3.connect(path) as con:
        query = con.cursor()
        query.execute(f"""SELECT command, date, hotels
                        FROM users
                        WHERE user_id = {user_id}
                        ORDER BY id DESC;""")
        results = query.fetchmany(10)
        return results


