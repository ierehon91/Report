import requests
import json
from pprint import pprint

from app.date_formats.date_formats import get_str_date_2
import app.config as config


class UpdateESIA:
    def __init__(self, url_id):
        self.google_sheet_url_id = url_id
        self.session = requests.Session()

    def __get_url(self):
        return f'https://spreadsheets.google.com/feeds/list/{self.google_sheet_url_id}/1/public/values?alt=json'

    def __get_esia_all_dates_journal(self):
        request = self.session.get(url=self.__get_url())
        journal = json.loads(request.text)['feed']['entry']
        return journal

    def get_esia_journal(self, year, month, day):
        esia_data = []
        for row in self.__get_esia_all_dates_journal():
            date = row['gsx$дата']['$t']
            specialist = row['gsx$специалист']['$t']
            event = row['gsx$учетноедействие']['$t']
            for parse_day in range(1, day + 1):
                parse_date = get_str_date_2(year, month, parse_day)
                if date == f'{parse_date}' and specialist and event:
                    esia_data.append({'date': date, 'specialist': specialist, 'event': event})
        return esia_data


def main():
    day = 28
    month = 7
    year = 2021
    esia = UpdateESIA(config.esia_url_id)
    return esia.get_esia_journal(year, month, day)


if __name__ == '__main__':
    pprint(main())
