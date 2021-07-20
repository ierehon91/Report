import requests
import json
from pprint import pprint
import app.config as config


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

    def set_report_params(self,
                          first_year, first_month, first_day,
                          last_year, last_month, last_day,
                          page_size=1000, num_page=0
                          ):
        page_size = str(page_size)
        num_page = str(num_page)
        self.report_url = f'http://{self.origin_url}/elq_frontoffice/supervisor/appointments?' \
                          f'&page={num_page}' \
                          f'&pageSize={page_size}' \
                          f'&recordDateFrom={first_year}-{first_month}-{first_day}+00:00' \
                          f'&recordDateTo={last_year}-{last_month}-{last_day}+23:59'

    def _get_report_object(self) -> object:
        return self.session.get(self.report_url)

    def get_report_json(self):
        report = self._get_report_object()
        return json.loads(report.text)['content']

    def _get_services_object(self):
        get_services_url = f'http://{self.origin_url}/elq_frontoffice/supervisor/serviceGroups?' \
                           f'page=0&' \
                           f'pageSize=50'
        return self.session.get(url=get_services_url)

    def get_services_json(self):
        services = self._get_services_object()
        return json.loads(services.text)['content']

    def _get_operators_object(self):
        get_operators_url = f'http://{self.origin_url}/elq_frontoffice/supervisor/operators?' \
                            f'excludeHistories=false' \
                            f'&page=0' \
                            f'&pageSize=50'
        return self.session.get(url=get_operators_url)

    def get_operators_json(self):
        operators = self._get_operators_object()
        return json.loads(operators.text)['content']

    def logout(self):
        self.session.get(f'http://{self.origin_url}/elq_frontoffice/supervisor/login?logout')


def main():
    eo = UpdateEO(config.eo_url)
    eo.authorization(config.eo_login, config.eo_password)
    eo.set_report_params(2021, 7, 1, 2021, 7, 20)
    report = eo.get_report_json()
    eo.logout()
    return report


if __name__ == '__main__':
    main()



