import os
import psycopg2

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_vacancies_with_keyword(keyword):
    """Получаем список всех вакансий, содержащих ключевые слова"""
    conn_params = {
        'host': DB_HOST,
        'database': DB_NAME,
        'user': DB_USER,
        'password': DB_PASSWORD
    }

    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies "
                            f"WHERE lower(vacancies_name) LIKE %s "
                            f"OR lower(vacancies_name) LIKE %s "
                            f"OR lower(vacancies_name) LIKE %s ",
                            (f'%{keyword}%', f'%{keyword}', f'{keyword}%'))
                result = cur.fetchall()

    except psycopg2.Error as e:
        print(f"Ошибка при запросе данных: {e}")
        return []
    return result


class DBManager:
    """Класс для подключения к БД"""

    def get_companies_and_vacancies_count(self):
        """Получаем список компаний и
         вакансий"""

        conn_params = {
            'host': DB_HOST,
            'database': DB_NAME,
            'user': DB_USER,
            'password': DB_PASSWORD
        }

        try:
            with psycopg2.connect(**conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT company_name, COUNT(vacancies_name) AS count_vacancies  "
                                f"FROM employers "
                                f"JOIN vacancies USING (employer_id) "
                                f"GROUP BY employers.company_name")
                    result = cur.fetchall()

        except psycopg2.Error as e:
            print(f"Ошибка при запросе данных: {e}")
            return []
        return result

    def get_all_vacancies(self):
        """Получаем список вакансий с названием компании,
    вакансии,зарплаты и ссылки на вакансию"""
        conn_params = {
            'host': "localhost",
            'database': "hh",
            'user': "postgres",
            'password': "2182"
        }

        try:
            with psycopg2.connect(**conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT employers.company_name, vacancies.vacancies_name, "
                                f"vacancies.payment, vacancies_url "
                                f"FROM employers "
                                f"JOIN vacancies USING (employer_id)")
                    result = cur.fetchall()

        except psycopg2.Error as e:
            print(f"Ошибка при запросе данных: {e}")
            return []
        return result

    def get_avg_salary(self):
        """Получаем среднюю заработную плату"""
        conn_params = {
            'host': DB_HOST,
            'database': DB_NAME,
            'user': DB_USER,
            'password': DB_PASSWORD
        }

        try:
            with psycopg2.connect(**conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT AVG(payment) as avg_payment FROM vacancies ")
                    result = cur.fetchall()

        except psycopg2.Error as e:
            print(f"Ошибка при запросе данных: {e}")
            return []
        return result

    def get_vacancies_with_higher_salary(self):
        """Получаем список вакансий с зарплатой выше средней"""
        conn_params = {
            'host': DB_HOST,
            'database': DB_NAME,
            'user': DB_USER,
            'password': DB_PASSWORD
        }

        try:
            with psycopg2.connect(**conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT * FROM vacancies "
                                f"WHERE payment > (SELECT AVG(payment) FROM vacancies) ")
                    result = cur.fetchall()

        except psycopg2.Error as e:
            print(f"Ошибка при запросе данных: {e}")
            return []
        return result
