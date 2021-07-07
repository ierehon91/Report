from datetime import datetime


def get_str_date_1(year: int, month: int, day: int) -> str:
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


def get_str_date_2(year, month, day):
    """Преобразовывает дату в строку формата дд.мм.гггг"""
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    year = str(year)
    return f'{day}.{month}.{year}'


def transform_date_to_int(year, month, day) -> int:
    """Преобразовывает дату в целочисленное значение"""
    dt = datetime(year, month, day)
    return int(round(dt.timestamp() * 1000))
