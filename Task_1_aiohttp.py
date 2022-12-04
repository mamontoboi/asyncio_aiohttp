# Завдання 1
# Створіть співпрограму, яка отримує контент із зазначених посилань і логує хід виконання в database,
# використовуючи стандартну бібліотеку requests, а потім проробіть те саме з бібліотекою aiohttp.
# Кроки, які мають бути залоговані: початок запиту до адреси X, відповідь для адреси X отримано зі статусом 200.
# Перевірте хід виконання програми на >3 ресурсах і перегляньте послідовність запису логів в обох варіантах
# і порівняйте результати. Для двох видів завдань використовуйте різні файли для логування,
# щоби порівняти отриманий результат.

import asyncio
import aiohttp
from datetime import datetime
import sqlite3


async def get_response(session, url):
    async with session.get(url) as req:
            start = datetime.now()
            await req.text()
            if req.status == 200:
                end = datetime.now()
                await insert_data(url, start, end)
                print(f'{url} response was successfully measured.')


async def get_tasks(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_response(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def main(urls):
    async with aiohttp.ClientSession() as session:
        await get_tasks(session, urls)
        print('The program is successfully competed.')


def create_db():
    try:
        sql_connection = sqlite3.connect("Task_1.db")
        cursor = sql_connection.cursor()

        sql_query = """CREATE TABLE "aiohttp requests" (
                        url TEXT NOT NULL,
                        "request time" timestamp PRIMARY KEY,
                        "response time" timestamp);
                        """

        cursor.execute(sql_query)

        sql_connection.commit()
        print("Database was successfully created.")

    except sqlite3.Error as e:
        print(f"The following exception has occurred: {e}.")

    finally:
        if sql_connection:
            sql_connection.close()
            print("The Database was closed.")


async def insert_data(url, start, end):
    try:
        sql_connection = sqlite3.connect('Task_1.db')
        cursor = sql_connection.cursor()

        sql_query = """INSERT INTO "aiohttp requests" 
                        (url, "request time", "response time")
                        VALUES (:url, :start, :end);"""

        data = {'url': url, 'start': start, 'end': end}
        cursor.execute(sql_query, data)

        sql_connection.commit()
        print("Data was successfully inserted.")

    except sqlite3.Error as e:
        print(f'The following problem has occurred: {e}.')
    finally:
        if sql_connection:
            sql_connection.close()


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

    asyncio.run(main(urls))
