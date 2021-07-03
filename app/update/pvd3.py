from requests import Session
from datetime import datetime
import re
from app.date_formats.date_formats import get_str_date
from pprint import pprint


def _get_services(filter_data):
    services = []
    for filter_row in filter_data:
        services.append(filter_row[2])
    services = set(services)
    return services


class UpdatePvd3(Session):
    """Класс получения данных из ПК ПВД 3"""
    def __init__(self, url, username, password, filial_number):
        self.url = url
        self.username = username
        self.password = password
        self.filial_number = filial_number
        self.session = Session()

    def _transform_date_to_int(self, year, month, day) -> int:
        """Преобразовывает дату в целочисленное значение"""
        dt = datetime(year, month, day)
        return int(round(dt.timestamp() * 1000))

    def _get_login_url(self) -> str:
        """Возвращает url адрес авторицации в ПК ПВД 3"""
        return rf'http://{self.url}/api/rs/login'

    def _get_report_url(self) -> str:
        """Возвращает url адрес формирования очётов в ПК ПВД 3"""
        return rf'http://{self.url}/api/rs/reports/execute'

    def _get_login_data(self) -> dict:
        """Возвращает словарь с логином и паролем для авторизации в ПК ПВД 3"""
        return {'username': self.username, 'password': self.password}

    def _get_report_data(self, year, month, day) -> dict:
        """Возвращает словарь с данными для составления отчёта в ПК ПВД 3 по форме Список обращений"""
        return {
            'file': 'Список обращений.jrd',
            'output': 'csv',
            'params':
                [
                    {'label': 'Начало периода', 'name': 'start', 'required': True, 'type': 'DATE',
                     'value': self._transform_date_to_int(year, month, day)},
                    {'label': 'Конец периода', 'name': 'end', 'required': True, 'type': 'DATE',
                     'value': self._transform_date_to_int(year, month, day)},
                    {'label': 'Код организации', 'name': 'num', 'required': False, 'type': 'STRING',
                     'value': self.filial_number}
                ]
        }

    def _parse_pvd_data(self, year, month, day):
        self.session.post(url=self._get_login_url(), data=self._get_login_data())
        return self.session.post(url=self._get_report_url(), json=self._get_report_data(year, month, day)).text

    def _get_list_data(self, year, month, day):
        data = []
        pvd_text = self._parse_pvd_data(year, month, day).split('\n')
        for i in range(3, len(pvd_text) - 1):
            row = pvd_text[i].split(',')
            data.append(row)
        return data

    def _filter_data(self, year, month, day):
        no_filter_data = self._get_list_data(year, month, day)
        filter_data = []
        for row in no_filter_data:
            date = row[3]
            user = row[2]
            service = row[5]
            kuvi_kuvd_text = ''.join(row[6:])
            count_reception = len(re.findall('КУВИ', kuvi_kuvd_text)) + len(re.findall('КУВД', kuvi_kuvd_text))
            filter_data.append((date, user, service, count_reception))
        return filter_data

    def _get_users(self, filter_data):
        users = []
        for filter_row in filter_data:
            users.append(filter_row[1])
        users = set(users)
        return users

    def get_pvd_data(self, year, month, day):
        filter_data = self._filter_data(year, month, day)
        users = self._get_users(filter_data)
        services = _get_services(filter_data)
        date = get_str_date(year, month, day)
        data = []
        for user in users:
            for service in services:
                all_count = 0
                for row in filter_data:
                    if user == row[1] and service == row[2]:
                        all_count += 1
                if all_count > 0:
                    data.append({'date_reception': date,
                                 'user': user,
                                 'service': service,
                                 'count_reception': all_count,
                                 'program_name': 'ПК ПВД 3'
                                 })
        return data


pvd3_url = '10.36.35.13'
pvd3_username = 'i.merkulov',
pvd3_password = 'zmr00A'
pvd3_filial_number = 'MFC-000002595'

pvd3_data = UpdatePvd3(pvd3_url, pvd3_username, pvd3_password, pvd3_filial_number)
pprint(pvd3_data.get_pvd_data(2021, 7, 2))
