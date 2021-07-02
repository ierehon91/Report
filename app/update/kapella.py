import csv
import os
import codecs
from pprint import pprint


class UpdateKapella():
    """Класс обработки данных csv файла, сформированного из АИС Капелла"""
    def __init__(self, path, delimiter):
        self.file_path = os.path.abspath(path)  # путь к csv файлу
        self.delimiter = delimiter  # символ разделитель в csv файле

    def _get_str_date(self, year: int, month: int, day: int) -> str:
        """Преобразовывает дату в строку формата гггг-мм-дд"""
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

    def _open_csv_file(self) -> list:
        """Открывает файл csv и возвращает его содержимое в виде списка"""
        with codecs.open(self.file_path, 'rU', 'utf-16') as r_file:
            return list(csv.reader(r_file, delimiter=self.delimiter))

    def get_data(self, year: int, month: int, day: int) -> list:
        """Приём документов за определенную дату из АИС Капелла."""
        file_reader = self._open_csv_file()
        last_user = ''
        data = []
        for row in file_reader:
            one_record = {}
            one_record['date_reception'] = self._get_str_date(year, month, day)  # дата приёма
            # Если в csv файле отсутвует специалист, то в словарь необходимо добавить специалиста из предыдущей итерации
            if row[0] != '':
                one_record['user'] = last_user = row[0]
            else:
                one_record['user'] = last_user
            one_record['service'] = row[1]  # название услуги
            one_record['count_reception'] = int(row[3])  # количество принятых дел
            one_record['program_name'] = 'АИС Капелла'  # название программы
            data.append(one_record)
        return data


kapella = UpdateKapella('test.csv', '$')
pprint(kapella.get_data(2021, 6, 30))
