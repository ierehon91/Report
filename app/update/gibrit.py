import requests
import json
from app.date_formats.date_formats import get_str_date_2


class UpdateGibrit():
    """Класс для получения данных системы Гибрит"""
    def __init__(self, url):
        self.url = url
        self.login: str = ''
        self.password: str = ''
        self.session: object
        self.session = requests.Session()

    def _get_login_url(self) -> str:
        return f'http://{self.url}/login'

    def _login_data(self, login, password):
        self.login = login
        self.password = password
        return {'username': f'{self.login}', 'password': f'{self.password}'}

    def authorization_gibrit(self, login, password):
        self.session.post(url=self._get_login_url(), data=self._login_data(login, password))

    def _get_report_url(self, year, month, day):
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

    def _get_parse_data(self, year, month, day):
        return self.session.get(url=self._get_report_url(year, month, day))

    def get_gibrit_data(self, year, month, day):
        data = self._get_parse_data(year, month, day)
        return json.loads(data.text)

    def close(self):
        self.session.get(f'http://{self.url}/logout')


class ParseGibritDate():
    pass
