import csv
import os
import codecs


class UpdateKapella():
    def __init__(self, path, delimiter):
        self.file_path = os.path.abspath(path)
        self.delimiter = delimiter

    def _get_str_date(self, year, month, day):
        """Преобразовывает дату в строку для дальнейшего парсинга данных"""
        if day >= 10:
            day = str(day)
        else:
            day = '0' + str(day)
        if month >= 10:
            month = str(month)
        else:
            month = '0' + str(month)
        year = str(year)
        return f'{year}-{month}-{day}'

    def _open_csv_file(self):
        with codecs.open(self.file_path, 'rU', 'utf-16') as r_file:
            return list(csv.reader(r_file, delimiter=self.delimiter))

    def get_data(self, year, month, day):
        file_reader = self._open_csv_file()
        last_user = ''
        data = []
        for row in file_reader:
            one_record = {}
            one_record['date_reception'] = self._get_str_date(year, month, day)
            if row[0] != '':
                one_record['user'] = last_user = row[0]
            else:
                one_record['user'] = last_user
            one_record['service'] = row[1]
            one_record['count_reception'] = row[3]
            data.append(one_record)
        return data


kapella_data = UpdateKapella('test.csv', '$')
print(kapella_data.get_data(2021, 6, 30))
