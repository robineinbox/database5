import psycopg2
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

db_config = {
    'host': config['database']['host'],
    'database': config['database']['database'],
    'user': config['database']['user'],
    'password': config['database']['password']
}

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(**db_config)

    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
            # Фиксация внесенных изменений в базу данных
            self.conn.commit()
        else:
            cursor.execute(query)
            # Фиксация внесенных изменений в базу данных
            self.conn.commit()
        if cursor.description:
            return cursor.fetchall()
        else:
            return None

    def insert_vacancy(self, company_id, vacancy_name, salary, vacancy_link):
        query = "INSERT INTO vacancies (company_id, vacancy_name, salary, vacancy_link) VALUES (%s, %s, %s, %s)"
        self.execute_query(query, (company_id, vacancy_name, salary, vacancy_link))

    def insert_employer(self, name, description):
        query = "INSERT INTO employers (name, description) VALUES (%s, %s)"
        self.execute_query(query, (name, description))

    def get_companies_and_vacancies_count(self):
        query = "SELECT company_id, COUNT(*) FROM vacancies GROUP BY company_id"
        return self.execute_query(query)

    def get_all_vacancies(self):
        query = "SELECT company_id, vacancy_name, salary, vacancy_link FROM vacancies"
        return self.execute_query(query)

    def get_avg_salary(self):
        query = "SELECT AVG(salary) FROM vacancies"
        return self.execute_query(query)[0][0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        query = "SELECT company_id, vacancy_name, salary, vacancy_link FROM vacancies WHERE salary > %s"
        return self.execute_query(query, (avg_salary,))

    def get_vacancies_with_keyword(self, keyword):
        query = "SELECT company_id, vacancy_name, salary, vacancy_link FROM vacancies WHERE vacancy_name ILIKE %s"
        return self.execute_query(query, ('%{}%'.format(keyword),))

    def close(self):
        self.conn.close()
