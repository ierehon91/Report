from requests import Session
import re
from app.date_formats.date_formats import get_str_date_1, transform_date_to_int
import app.config as config


class UpdatePvd3:
    """Класс получения данных из ПК ПВД 3"""
    def __init__(self, url):
        self.url = url
        self.username = ''
        self.password = ''
        self.filial_number = ''
        self.session = Session()

    def __get_login_url(self) -> str:
        """Возвращает url адрес авторицации в ПК ПВД 3"""
        return rf'http://{self.url}/api/rs/login'

    def __get_login_data(self, username, password) -> dict:
        """Возвращает словарь с логином и паролем для авторизации в ПК ПВД 3"""
        self.username = username
        self.password = password
        return {'username': self.username, 'password': self.password}

    def authorization(self, username, password):
        request = self.session.post(url=self.__get_login_url(), data=self.__get_login_data(username, password))
        return request

    def __get_report_url(self) -> str:
        """Возвращает url адрес формирования очётов в ПК ПВД 3"""
        return rf'http://{self.url}/api/rs/reports/execute'

    def set_filial_number(self, filial_number):
        """Задаётся номер филиала"""
        self.filial_number = filial_number

    def __get_report_data(self, year, month, day) -> dict:
        """Возвращает словарь с данными для составления отчёта в ПК ПВД 3 по форме Список обращений"""
        date_reception = transform_date_to_int(year, month, day)
        return {
            'file': 'Список обращений.jrd',
            'output': 'csv',
            'params':
                [
                    {'label': 'Начало периода', 'name': 'start', 'required': True, 'type': 'DATE',
                     'value': date_reception},
                    {'label': 'Конец периода', 'name': 'end', 'required': True, 'type': 'DATE',
                     'value': date_reception},
                    {'label': 'Код организации', 'name': 'num', 'required': False, 'type': 'STRING',
                     'value': self.filial_number}
                ]
        }

    def __parse_pvd_data(self, year, month, day):
        """request метод для получения данных"""
        return self.session.post(url=self.__get_report_url(), json=self.__get_report_data(year, month, day)).text

    def __get_list_data(self, year, month, day):
        """Разделение текста, полученного из ПК ПВД 3 на списки"""
        data = []
        pvd_text = self.__parse_pvd_data(year, month, day).split('\n')
        for i in range(3, len(pvd_text) - 1):
            row = pvd_text[i].split(',')
            data.append(row)
        return data

    def __filter_data(self, year, month, day):
        """Удаляются лишние данные в списке, ведётся подсчёт количества КУВИ и КУВД в одном обращении"""
        no_filter_data = self.__get_list_data(year, month, day)
        filter_data = []
        for row in no_filter_data:
            date = row[3]
            user = row[2]
            service = row[5]
            kuvi_kuvd_text = ''.join(row[6:])
            count_reception = len(re.findall('КУВИ', kuvi_kuvd_text)) + len(re.findall('КУВД', kuvi_kuvd_text))
            filter_data.append((date, user, service, count_reception))
        return filter_data

    def __get_users(self, report_data):
        """Множество сотрудников, принявшие обращения"""
        users = []
        for filter_row in report_data:
            users.append(filter_row[1])
        users = set(users)
        return users

    def __get_services(self, report_data):
        """Множество названий услуг, по которым велось обращение"""
        services = []
        for filter_row in report_data:
            services.append(filter_row[2])
        services = set(services)
        return services

    def get_report(self, year, month, day) -> list:
        """Приём документов за определенную дату из ПК ПВД 3."""
        filter_data = self.__filter_data(year, month, day)
        users = self.__get_users(filter_data)
        services = self.__get_services(filter_data)
        date = get_str_date_1(year, month, day)
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


def main():
    day = 27
    month = 7
    year = 2021
    pvd = UpdatePvd3(config.pvd3_url)
    pvd.authorization(config.pvd3_username, config.pvd3_password)
    pvd.set_filial_number(config.pvd3_filial_alias)
    return pvd.get_report(year, month, day)


if __name__ == '__main__':
    main()
