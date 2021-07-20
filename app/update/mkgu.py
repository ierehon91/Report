import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint

from app.date_formats.date_formats import get_str_date_1
import app.config as config


class UpdateMKGU:
    """Клас получения данных из системы МКГУ Ваш Контроль"""

    def __init__(self):
        self.session = requests.Session()
        self.origin_url = 'https://vashkontrol.ru'
        self.login_url = f'{self.origin_url}/users/sign_in'
        self.filial_url = f'{self.origin_url}/hershel/regions/20/reports/general'
        self.report_url = f'{self.origin_url}/hershel/regions/20/reports/general/submit'
        self.logout_url = f'{self.origin_url}/users/sign_out'

    def _get_token(self, url) -> str:
        """Метод получения уникального csrf токена для дальнейшего экспорта в тело запроса"""
        request_token = self.session.get(url)
        csrf_token = re.findall(r"[^\"\>\{\}\\]{86}==", request_token.text)  # вычленяем csrf_token из тела страницы
        return csrf_token[0]

    def _get_login_data(self, login: str, password: str) -> dict:
        """Возвращает словарь для авторизации на сервере"""
        login_data = {'user[login]': login,
                      'user[password]': password,
                      'authenticity_token': self._get_token(self.login_url)
                      }
        return login_data

    def authorization(self, login: str, password: str):
        """Авторизация по логину и пароля на сервере"""
        self.session.post(url=self.login_url, data=self._get_login_data(login, password))

    def _get_headers(self):
        """Возвращает headers для парсинга отчёта"""
        headers = {
            'x-csrf-token': self._get_token(self.filial_url),
            'x-requested-with': 'XMLHttpRequest',
            'origin': self.origin_url,
            'referer': self.report_url,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }
        return headers

    def _get_reception_request_data(self,
                                    first_year: int, first_month: int, first_day: int,
                                    last_year: int, last_month: int, last_day: int
                                    ) -> str:
        """Возвращает строку с телом запроса для получения отчёта"""

        first_date = get_str_date_1(first_year, first_month, first_day)
        last_date = get_str_date_1(last_year, last_month, last_day)

        reception_request_data = 'report_type=custom' \
                         '&year=2021' \
                         '&quarter=1' \
                         '&month=1' \
                         f'&date_start={first_date}' \
                         f'&date_end={last_date}' \
                         '&category_ids%5B%5D=4' \
                         '&category_ids%5B%5D=5' \
                         '&category_ids%5B%5D=1' \
                         '&category_ids%5B%5D=2' \
                         '&category_ids%5B%5D=3' \
                         '&mfc_ids%5B%5D=all' \
                         '&service_type=all' \
                         '&service_ids%5B%5D=all'
        return reception_request_data

    def _get_report_object(self,
                           first_year: int, first_month: int, first_day: int,
                           last_year: int, last_month: int, last_day: int
                           ) -> object:
        """Получает и возвращает объект запроса с отчётом"""

        report = self.session.post(url=self.report_url,
                                   headers=self._get_headers(),
                                   data=self._get_reception_request_data(first_year, first_month, first_day,
                                                                         last_year, last_month, last_day)
                                   )
        return report

    def get_report(self,
                   first_year: int, first_month: int, first_day: int,
                   last_year: int, last_month: int, last_day: int
                   ) -> dict:
        """Возвращает отчёт за указанный период"""

        report_object = self._get_report_object(first_year, first_month, first_day, last_year, last_month, last_day)
        soup = BeautifulSoup(report_object.text, 'html.parser')
        soup = soup.get_text()
        report_soup = soup.split('<\/td>')

        return {'filial_name': report_soup[1].split('<')[0],
                'count_phone_numbers': int(report_soup[2].split('<')[0]),
                'count_factors': int(report_soup[3].split('<')[0]),
                'all_scores': int(report_soup[4].split('<')[0]),
                'score_1': int(report_soup[5].split('<')[0]),
                'score_2': int(report_soup[6].split('<')[0]),
                'score_3': int(report_soup[7].split('<')[0]),
                'score_4': int(report_soup[8].split('<')[0]),
                'score_5': int(report_soup[9].split('<')[0]),
                'rating': float(report_soup[10].split('<')[0])
                }

    def logout(self):
        """logout на сервере"""

        logout_data = {
            '_method': 'delete',
            'authenticity_token': self._get_token(self.filial_url)
        }
        self.session.post(url=self.logout_url, data=logout_data)


def parse_all_mkgu_data(mkgu_accounts,
                        first_year, first_month, first_day,
                        last_year, last_month, last_day
                        ) -> list:
    mkgu = UpdateMKGU()
    reports = []
    for account in mkgu_accounts[:1]:
        print('Парсим: ' + account['name'])
        mkgu.authorization(account['login'], account['password'])
        reports.append(mkgu.get_report(first_year, first_month, first_day, last_year, last_month, last_day))
        mkgu.logout()
    return reports


def main():
    return parse_all_mkgu_data(config.mkgu_accounts, 2021, 7, 1, 2021, 7, 17)


if __name__ == '__main__':
    print(main())
