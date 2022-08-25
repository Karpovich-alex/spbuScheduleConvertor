import datetime as dt
import pandas as pd


def parse_dates(dates):
    if type(dates) == pd.core.arrays.datetimes.DatetimeArray:
        # dates = dates.reset_index(drop=True)
        return find_pattern(dates)
    else:
        return [(dates, dates, 1, '')]


def find_pattern(dates):
    output_data = []
    date_start = dates[0]
    date_end = dates[0]
    repeat_time = 1
    repeat_type = 'weekly'
    for date in dates[1:]:
        if (date_end + dt.timedelta(days=7) == date and repeat_type == 'weekly') or (
                date_end + dt.timedelta(days=14) == date and repeat_type == 'biweekly'):
            date_end = date
            repeat_time += 1
        else:
            if date_end + dt.timedelta(days=7) == date:
                if repeat_time == 1:
                    repeat_time += 1
                    date_end = date
                    repeat_type = 'weekly'
                    continue
                output_data.append((date_start, date_end, repeat_time, repeat_type))
                date_start, date_end, repeat_time, repeat_type = date, date, 1, 'weekly'
                continue
            if date_end + dt.timedelta(days=14) == date:
                if repeat_time == 1:
                    repeat_time += 1
                    date_end = date
                    repeat_type = 'biweekly'
                    continue
                output_data.append((date_start, date_end, repeat_time, repeat_type))
                date_start, date_end, repeat_time, repeat_type = date, date, 1, 'biweekly'
                continue
            if date_end == date:
                continue
            output_data.append((date_start, date_end, repeat_time, repeat_type))
            date_start, date_end, repeat_time = date, date, 1
    output_data.append((date_start, date_end, repeat_time, repeat_type))
    return output_data


def parse_time(time_str):
    def get_datetime_format(time_str: str):
        return pd.to_datetime(time_str, format='%H:%M').time()

    return list(map(get_datetime_format, time_str.split('–')))