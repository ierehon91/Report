# Отчёты МФЦ
## Получение данных за день
Источники получения данных:

 - АИС Капелла
 - ПК ПВД 3
 - Сбербанк Гибрид
 - ЭО "Фронтофис"
 - МКГУ "Ваш Контроль"
 - Журнал ЕСИА

Модуль, который отвечает за парсинг данных и источников находится:
***app/update/***

### АИС Капелла
Данные из АИС Капелла содержат количество принятых услуг по определенной услуге определенным специалистом за указанный период времени.
Так как невозможно использовать request методы для получения данных напрямую из системы АИС Капелла, целесообразно изначально выгрузить их в формате csv вручную в определенную директорию, а далее произвести парсинг данного файла.

Для того чтобы выгрузить данные из Капеллы, необходимо в АИС:
1. Перейти в раздел Отчёты
2. Выбрать "Количество обращений заявителей по операторам"
3. Указать период и подразделение
4. Сохранить полученный отчёт формата Data File
5. В настройках указать Type - **csv**, разделитель - например знак **$** и Band Filter - **Data only**. Установить галочку "Пропускать заголовки колонок"
6. Нажать ОК и выбрать папку для сохранения.

#### Работа в Проекте Отчёты МФЦ

За получения данных из csv отвечает класс `UpdateKapella` модуля `app.update.kapella`
| Тип  | Название | Описание | Параметры | Пример |
|--|--|--|--|--|
| Класс | UpdateKapella | Класс получения данных из csv | Путь к csv файлу, символ разделитель| `kapella = UpdateKapella('temp\file.csv', delimiter='$')` |
| Метод | get_data | Возвращает список с данными из csv | Год, Месяц, День | `kapella.get_data(2021, 7, 12)` |

Пример получения данных:
```python
# Создаём экземпляр объекта kapella
# Аргумент delimiter указывает на символ, который указывали в качестве разделителя при сохранении отчёта в АИС
kapella = UpdateKapella(r'\temp\kapella_data.csv', delimiter='$')
# Получаем данные за 12.07.2021
kapella_data = kapella.get_data(2021, 7, 12)
```
Формируется список, где каждая запись представлена в виде словаря:
```python
    {'date_reception': 'Дата в формате гггг-мм-дд', 
    'user': 'ФИО или название пользователя в системе АИС Капелла', 
    'service': 'Название услуги', 
    'count_reception': 'Кол-во дел принято', 
    'program_name': 'АИС Капелла'
    }
```
### ПК ПВД 3
Данные из ПК ПВД 3 содержат количество принятых заявлений (КУВД и КУВИ) по услугам Росреестра определенным специалистом за указанный период времени.
Получение данных происходит непосредственно с сервера ПК ПВД 3, для этого используется библиотека requests.
За получения данных отвечает класс `UpdatePvd3` модуля `app.update.pvd3'

За получения данных из csv отвечает класс `UpdateKapella` модуля `app.update.kapella`

| Тип | Название | Описание | Параметры | Пример | Комментарий |
|--|--|--|--|--|--|
| Класс | UpdatePvd3 | Класс получения данных из ПК ПВД 3 | Адрес сервера | `pvd = UpdatePvd3('10.36.35.13')` |
| Метод | authorization | Авторизация в системе ПК ПВД 3 | Логин, пароль | `pvd.authorization('login', 'password')` |
| Метод | set_filial_number| Указатель филиала  | Код филиала | `pvd.set_filial_number('MFC-000002595')` | Если не вызывать данный метод у экземпляра, получение данных будет производиться по всем филиалам на сервере |
| Метод | get_pvd_data| Указатель филиала | Год, Месяц, День | `pvd.get_pvd_data(2021, 7, 12)` | 

Пример получения данных:
```python
# Создаём экземпляр объекта pvd
pvd = UpdatePvd3('10.36.35.13')
# Авторизация на сервере
pvd.authorization('login', 'password')
# Указываем код филиала
pvd.set_filial_number('MFC-000002595')
# Получаем данные за 12.07.2021
pvd_data = pvd.get_pvd_data(2021, 7, 12)
```
Формируется список, где каждая запись представлена в виде словаря:
```python
    {'date_reception': 'Дата в формате гггг-мм-дд', 
    'user': 'ФИО или название пользователя в системе ПК ПВД 3', 
    'service': 'Название услуги', 
    'count_reception': 'Кол-во дел принято', 
    'program_name': 'ПК ПВД 3'
    }
```