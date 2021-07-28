import csv
import os
import codecs

from app.date_formats.date_formats import get_str_date_1
import app.config as config

class UpdateKapella:
    """Класс получения данных csv файла, сформированного из АИС Капелла"""
    def __init__(self, path, delimiter):
        self.file_path = os.path.abspath(path)  # путь к csv файлу
        self.delimiter = delimiter  # символ разделитель в csv файле

    def __open_csv_file(self) -> list:
        """Открывает файл csv и возвращает его содержимое в виде списка"""
        with codecs.open(self.file_path, 'rU', 'utf-16') as r_file:
            return list(csv.reader(r_file, delimiter=self.delimiter))

    def get_report(self, year: int, month: int, day: int) -> list:
        """Приём документов за определенную дату из АИС Капелла."""
        try:
            file_reader = self.__open_csv_file()
        except FileNotFoundError:
            print(f"Файл {self.file_path} не найден.")
        else:
            last_user = ''
            data = []
            for row in file_reader:
                one_record = {}
                one_record['date_reception'] = get_str_date_1(year, month, day)  # дата приёма
                # Если в csv файле отсутствует специалист, то в словарь необходимо добавить специалиста
                # из предыдущей итерации.
                if row[0] != '':
                    one_record['user'] = last_user = row[0]
                else:
                    one_record['user'] = last_user
                one_record['service'] = row[1]  # название услуги
                one_record['count_reception'] = int(row[3])  # количество принятых дел
                one_record['program_name'] = 'АИС Капелла'  # название программы
                data.append(one_record)
            return data


def main():
    day = 14
    month = 7
    year = 2021
    kapella = UpdateKapella(r'..\..\temp\kapella_data.csv', delimiter=config.kapella_delimiter)
    return kapella.get_report(year, month, day)


if __name__ == '__main__':
    print(main())
