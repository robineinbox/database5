CREATE TABLE IF NOT EXISTS employers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS vacancies (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(100) NOT NULL,
    vacancy_name VARCHAR(100) NOT NULL,
    salary INTEGER,
    vacancy_link TEXT
);
