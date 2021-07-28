import requests
import json
from app.date_formats.date_formats import get_str_date_2
import app.config as config


class UpdateGibrit:
    """Класс для получения данных системы Гибрит"""
    def __init__(self, url):
        self.url = url
        self.login: str = ''
        self.password: str = ''
        self.session: object
        self.session = requests.Session()

    def __get_login_url(self) -> str:
        """Получение ссылки для авторизации"""
        return f'http://{self.url}/login'

    def __get_login_data(self, login, password):
        """Получение данных для авторизации"""
        self.login = login
        self.password = password
        return {'username': f'{self.login}', 'password': f'{self.password}'}

    def authorization(self, login, password):
        """Метод авторизации на сервере системы Гибрит"""
        self.session.post(url=self.__get_login_url(), data=self.__get_login_data(login, password))

    def __get_report_url(self, year, month, day):
        """Получение url для get запроса данных с сервера Гибрит"""
        report_url = f'http://{self.url}/hybrid/v2/check/analytics/all' \
                 '?sortField=paymentId' \
                 f'&fromPaymentDate={get_str_date_2(year, month, day)}' \
                 f'&toPaymentDate={get_str_date_2(year, month, day)}' \
                 '&statuses=PAYMENT_EXEC_CONFIRMED,' \
                 'PAYMENT_REVERSED,' \
                 'PAYMENT_REVERSE_NOT_FINISH,' \
                 'PAYMENT_MONEY_BACK,' \
                 'PAYMENT_ERROR_NOT_MONEY_BACK'
        return report_url

    def __get_parse_data(self, year: int, month: int, day: int) -> object:
        """Процесс парсинга данных из системы Гибрит"""
        return self.session.get(url=self.__get_report_url(year, month, day))

    def get_gibrit_data(self, year: int, month: int, day: int) -> list:
        """Получение данных из системы Гибрит для всех филиалов"""
        data = self.__get_parse_data(year, month, day)
        return json.loads(data.text)

    def get_filial_gibrit_data(self, year: int, month: int, day: int, filial_alias: str = '') -> list:
        """Получение данных из системы Гибрит для конкретного филиала"""
        filial_data = []
        for row in self.get_gibrit_data(year, month, day):
            if filial_alias in row['terminalName']:
                filial_data.append(row)
        return filial_data

    def close(self):
        """Выход из системы Гибрит"""
        self.session.get(f'http://{self.url}/logout')


def main():
    day = 14
    month = 7
    year = 2021
    gibrit = UpdateGibrit(config.gibrit_url)
    gibrit.authorization(config.gibrit_login, config.gibrit_password)
    gibrit_data = gibrit.get_filial_gibrit_data(year, month, day, filial_alias=config.gibrit_filial_alias)
    gibrit.close()
    return gibrit_data


if __name__ == '__main__':
    print(main())
