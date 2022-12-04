# Завдання 1
# Створіть співпрограму, яка отримує контент із зазначених посилань і логує хід виконання в database,
# використовуючи стандартну бібліотеку requests, а потім проробіть те саме з бібліотекою aiohttp.
# Кроки, які мають бути залоговані: початок запиту до адреси X, відповідь для адреси X отримано зі статусом 200.
# Перевірте хід виконання програми на >3 ресурсах і перегляньте послідовність запису логів в обох варіантах
# і порівняйте результати. Для двох видів завдань використовуйте різні файли для логування,
# щоби порівняти отриманий результат.

import requests
import sqlite3
from datetime import datetime


def request(urls):
    for url in urls:
        response = requests.get(url)
        start = datetime.now()
        if response.ok:
            end = datetime.now()
            insert_data(url, start, end)
            print(f'{url} response was successfully measured.')


def insert_data(url, start, end):
    try:
        sqlite_connection = sqlite3.connect("Task_1.db")
        cursor = sqlite_connection.cursor()

        sql_query = """INSERT INTO "requests requests" 
                        (url, "request time", "response time")
                        VALUES (:url, :start, :end);"""

        data = {"url": url, "start": start, "end": end}
        cursor.execute(sql_query, data)

        sqlite_connection.commit()
        print("Data was successfully inserted.")

    except sqlite3.Error as e:
        print(f"The following problem has occurred: {e}")

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def create_db():
    try:
        sql_connect = sqlite3.connect("Task_1.db")
        cursor = sql_connect.cursor()

        sql_query = """CREATE TABLE "requests requests"(
                        url TEXT NOT NULL,
                        "request time" timestamp PRIMARY KEY,
                        "response time" timestamp);
                        """

        cursor.execute(sql_query)

        sql_connect.commit()
        print("Database was successfully created.")

    except sqlite3.Error as e:
        print(f'The following problem was encountered: {e}.')

    finally:
        if sql_connect:
            sql_connect.close()
            print("The Database was closed.")


if __name__ == '__main__':
    create_db()
    urls = [
        'https://amp.dw.com/es/es-lo-correcto-20000-combatientes-extranjeros-se-han-alistado-para-luchar-en-ucrania-seg%C3%BAn-funcionarios/a-61073221',
        'https://en.wikipedia.org/wiki/Main_Page',
        'https://en.wikipedia.org/wiki/Paramount_leader',
        'https://es.wikipedia.org/wiki/Wikipedia:Portada',
        'https://es.wikipedia.org/wiki/Protestas_contra_el_confinamiento_por_la_pandemia_de_COVID-19_en_China',
        'https://es.wikipedia.org/wiki/Protestas_por_la_muerte_de_Mahsa_Amini',
        'https://uk.wikipedia.org/wiki/%D0%A2%D1%80%D0%B8%D0%B4%D0%B5%D0%BD%D1%82%D1%81%D1%8C%D0%BA%D0%B8%D0%B9_%D1%81%D0%BE%D0%B1%D0%BE%D1%80'
    ]
    request(urls)

