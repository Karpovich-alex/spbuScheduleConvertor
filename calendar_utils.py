from typing import List
import datetime as dt
import pandas as pd


def to_datetime(date: str, year: int):
    return dt.datetime.strptime(date + f'.{year}', "%d.%m.%Y").date()


def find_two_week_dates(dates) -> List:
    output_data = []
    date_start = dates[0]
    date_end = dates[0]
    repeat_time = 1
    repeat_type = 'biweekly'
    for date in dates:
        if date_end + dt.timedelta(days=14) == date:
            date_end = date
            repeat_time += 1
        else:
            if date_end == date:
                continue
            output_data.append((date_start, date_end, repeat_time, repeat_type))
            date_start, date_end, repeat_time = date, date, 1
    output_data.append((date_start, date_end, repeat_time, repeat_type))
    return output_data


def find_dates(x: str, year: int) -> List:
    if x.find('\n') != -1:
        dates = list(map(lambda date: to_datetime(date, year), x.split('\n')))
        return find_two_week_dates(dates)
    elif x[-1] == ')':
        dates, repeat_time = x.split('(')
        date_start, date_end = dates.strip().split('–')
        repeat_time = int(repeat_time[:-1])
        repeat_type = 'weekly'
    else:
        date_start = x
        date_end = x
        repeat_time = 1
        repeat_type = ''
    date_start = dt.datetime.strptime(date_start + f'.{year}', "%d.%m.%Y").date()
    date_end = dt.datetime.strptime(date_end + f'.{year}', "%d.%m.%Y").date()

    return [(date_start, date_end, repeat_time, repeat_type)]


def parse_date(x: str, year: int) -> List:
    if x.find('–') != -1 and x.find('\n') != -1:
        dates = []
        for date in x.split('\n'):
            dates += parse_date(date, year)
        return dates
    return find_dates(x, year)


def parse_time(time_str):
    def get_datetime_format(time_str: str):
        return pd.to_datetime(time_str, format='%H:%M').time()

    return list(map(get_datetime_format, time_str.split('–')))


def find_sub_group(subject: str):
    separation = '_x000d_\n'
    if subject.find(separation) != -1:
        subject_name, sub_group = subject.split(separation)
    else:
        subject_name, sub_group = subject, ''
    return sub_group


def test_find_sub_group():
    print(find_sub_group('Траектория 3 (В1 – В2). Английский язык, практическое занятие_x000d_\nПодгруппа 7'))


def test_parsing():
    CURRENT_YEAR = 2022
    print(parse_date('12.02–30.04 (12)', CURRENT_YEAR))
    print(parse_date('02.09–28.10 (9)\n11.11–09.12 (5)', CURRENT_YEAR))
    print(parse_date('01.09\n15.09\n29.09\n13.10\n27.10\n10.11', CURRENT_YEAR))
    print(parse_date('01.09\n15.09\n29.09\n27.10\n10.11', CURRENT_YEAR))
