import requests
import json
import app.config as config
from pprint import pprint
from app.date_formats.date_formats import str_to_int_time


class UpdateEO:
    def __init__(self, url):
        self.session = requests.Session()
        self.origin_url = url
        self.report_url = ''

    def _get_login_data(self, login, password):
        return {'username': login, 'password': password}

    def authorization(self, login, password):
        login_url = f'http://{self.origin_url}/elq_frontoffice/supervisor/loginProcess'
        self.session.post(url=login_url, data=self._get_login_data(login, password))

    def _get_elements(self, first_year, first_month, first_day,
                            last_year, last_month, last_day):
        get_elements_url = f'http://{self.origin_url}/elq_frontoffice/supervisor/appointments?' \
              f'page=0&pageSize=1' \
              f'&recordDateFrom={first_year}-{first_month}-{first_day}+00:00' \
              f'&recordDateTo={last_year}-{last_month}-{last_day}+23:00'
        elements = self.session.get(url=get_elements_url)
        return json.loads(elements.text)['totalElements']

    def set_report_params(self,
                          first_year, first_month, first_day,
                          last_year, last_month, last_day
                          ):
        page_size = str(self._get_elements(first_year, first_month, first_day, last_year, last_month, last_day))
        print(page_size)
        self.report_url = f'http://{self.origin_url}/elq_frontoffice/supervisor/appointments?' \
                          f'&page=0' \
                          f'&pageSize={page_size}' \
                          f'&recordDateFrom={first_year}-{first_month}-{first_day}+00:00' \
                          f'&recordDateTo={last_year}-{last_month}-{last_day}+23:59'

    def _get_report_object(self) -> object:
        return self.session.get(self.report_url)

    def _get_report_json(self):
        report = self._get_report_object()
        return json.loads(report.text)['content']

    def _get_services_object(self):
        get_services_url = f'http://{self.origin_url}/elq_frontoffice/supervisor/serviceGroups?' \
                           f'page=0&' \
                           f'pageSize=50'
        return self.session.get(url=get_services_url)

    def get_services(self):
        services = self._get_services_object()
        return json.loads(services.text)['content']

    def _get_operators_object(self):
        get_operators_url = f'http://{self.origin_url}/elq_frontoffice/supervisor/operators?' \
                            f'excludeHistories=false' \
                            f'&page=0' \
                            f'&pageSize=50'
        return self.session.get(url=get_operators_url)

    def get_operators(self):
        operators = self._get_operators_object()
        return json.loads(operators.text)['content']

    def get_report(self) -> list:
        tickets = []
        for row in self._get_report_json():
            ticket = {}
            try:
                ticket['ticket_id'] = row['id']
            except KeyError:
                ticket['ticket_id'] = None
            # Номер талона
            try:
                ticket['ticket_number'] = row['ticketcode']
            except KeyError:
                ticket['ticket_number'] = None
            # Статус талона
            try:
                ticket['ticket_status'] = row['recordstate']
            except KeyError:
                ticket['ticket_status'] = None
            # id Филиала
            try:
                ticket['filial_id'] = row['employee']['division']['id']
            except KeyError:
                ticket['filial_id'] = None
            # id Специалиста
            try:
                ticket['specialist_id'] = row['employee']['id']
            except KeyError:
                ticket['specialist_id'] = None
            # Окно
            try:
                ticket['window'] = row['operatorwindow']['name']
            except KeyError:
                ticket['window'] = None
            # Тип записи
            try:
                ticket['isprerecord'] = row['isprerecord']
            except KeyError:
                ticket['isprerecord'] = None
            # Приоритет
            try:
                ticket['priority'] = row['priority']
            except KeyError:
                ticket['priority'] = None
            # id Услуги
            try:
                ticket['service_id'] = row['servicegroup']['id']
            except KeyError:
                ticket['service_id'] = None
            # Время ожидания
            try:
                ticket['wait_time'] = str_to_int_time(row['waitTime'])
            except KeyError:
                ticket['wait_time'] = None
            # Дата и время постановки в очередь
            try:
                ticket['queue_date'] = row['queueDate']
            except KeyError:
                ticket['queue_date'] = None
            # Дата записи
            try:
                ticket['record_date'] = row['recorddate']
            except KeyError:
                ticket['record_date'] = None
            # Время записи
            try:
                ticket['record_time'] = row['recordtime']
            except KeyError:
                ticket['record_time'] = None
            # Фактическая дата время приёма
            try:
                ticket['actual_date'] = row['actualDate']
            except KeyError:
                ticket['actual_date'] = None
            # Фактическое время обслуживания
            try:
                ticket['actual_serving_time'] = row['actualServingTime']
            except KeyError:
                ticket['actual_serving_time'] = None
            # Дата время завершения записи
            try:
                ticket['state_date'] = row['statedate']
            except KeyError:
                ticket['state_date'] = None
            # Дата время создания записи
            try:
                ticket['create_date'] = row['createdate']
            except KeyError:
                ticket['create_date'] = None
            tickets.append(ticket)
            try:
                ticket['specialist_last_name'] = row['employee']['lastname']
            except KeyError:
                ticket['specialist_last_name'] = None
            try:
                ticket['service_name'] = row['servicegroup']['name']
            except KeyError:
                ticket['service_name'] = None

            tickets.append(ticket)
        return tickets

    def logout(self):
        self.session.get(f'http://{self.origin_url}/elq_frontoffice/supervisor/login?logout')


def main():
    eo = UpdateEO(config.eo_url)
    eo.authorization(config.eo_login, config.eo_password)
    eo.set_report_params(2021, 7, 20, 2021, 7, 20)
    report = eo.get_report()
    eo.logout()
    return report


if __name__ == '__main__':
    pprint(main())
