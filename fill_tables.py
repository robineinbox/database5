import psycopg2
import requests

import db_manager


def fill_employers_table():
    response = requests.get("https://api.hh.ru/employers")
    employers_data = response.json()

    connection = psycopg2.connect(
        host="localhost",
        database="course5",
        user="postgres",
        password="KimNikol2"
    )
    cursor = connection.cursor()

    for employer in employers_data["items"]:
        name = employer["name"]

        if "description" in employer:
            description = employer["description"]
        else:
            description = ""

        query = "INSERT INTO employers (name, description) VALUES (%s, %s);"
        cursor.execute(query, (name, description))

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    fill_employers_table()
