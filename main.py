import requests
from db_manager import DBManager

def run_main():
    companies = ['1740', '2180', '3529', '3112647', '362', '3093544', '22494', '78638', '54', '87021']
    db_manager = DBManager()
    unique_employers = set()
    for company in companies:
        url = f'https://api.hh.ru/vacancies?employer_id={company}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            vacancies = data['items']
            for vacancy in vacancies:
                if vacancy.get('salary') is not None:
                    salary = vacancy['salary'].get('from')
                else:
                    salary = None
                vacancy_name = vacancy['name']
                vacancy_link = vacancy['alternate_url']
                # Insert employer data into database
                employer = vacancy.get('employer')
                employer_name = employer.get('name') if employer else None
                employer_description = employer.get('description') if employer else None
                if employer_name not in unique_employers:
                    db_manager.insert_employer(employer_name, employer_description)
                    unique_employers.add(employer_name)
                db_manager.insert_vacancy(company, vacancy_name, salary, vacancy_link)
        else:
            print(f'Ошибка при получении данных о компании {company}. Статус-код:', response.status_code)

    for company, count in db_manager.get_companies_and_vacancies_count():
        print(f'{company}: {count} вакансий')

    vacancies_python = db_manager.get_vacancies_with_keyword('python')
    for vacancy in vacancies_python:
        print(vacancy)

    avg_salary = db_manager.get_avg_salary()
    print(f'Средняя зарплата: {avg_salary}')

    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    for vacancy in vacancies_with_higher_salary:
        print(vacancy)

    db_manager.close()

if __name__ == "__main__":
    run_main()
