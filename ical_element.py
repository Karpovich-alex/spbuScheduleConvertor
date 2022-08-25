import pytz
from icalendar import Calendar, Event
import pandas as pd
import datetime as dt


class Subject:
    params = ['TimeStart', 'TimeEnd', 'DateStart', 'DateEnd', 'SubjectName', 'Place', 'Teacher', 'RepeatTime',
              'RepeatType', 'SubGroup']
    tz = pytz.timezone('Europe/Moscow')

    def __init__(self, TimeStart, TimeEnd, DateStart, DateEnd, SubjectName, Place, Teacher, RepeatTime=1, RepeatType='',
                 SubGroup=None):
        self.time_start = TimeStart
        self.time_end = TimeEnd
        self.date_start = DateStart
        self.date_end = DateEnd
        self.subject_name = SubjectName if not SubGroup else SubjectName + '#' + f'{SubGroup}'
        self.place = Place
        self.teacher = Teacher
        self.repeat_time = RepeatTime
        self.repeat_type = RepeatType
        self.sub_group = SubGroup

    # @property
    # def time_start(self):
    #     return self._time_start
    #
    # @time_start.setter
    # def time_start(self, v):
    #     if type(v) == 'string':
    #         v =
    #     self._time_start = v
    @property
    def date_time_start_event(self):
        return self.get_date_time(self.date_start, self.time_start)

    @property
    def date_time_end_event(self):
        return self.get_date_time(self.date_start, self.time_end)

    @classmethod
    def get_date_time(cls, date, time):
        return dt.datetime.combine(date, time, cls.tz)

    @classmethod
    def from_series(cls, series: pd.Series):
        subject_params = [series[param] for param in cls.params]
        return cls(*subject_params)

    def __repr__(self):
        return f"<Subject time start: {self.time_start} date start: {self.date_start} with {self.repeat_time} repeat>"

    def to_event(self) -> Event:
        e = Event()
        e.add('DTSTART', self.date_time_start_event)
        e.add('DTEND', self.date_time_end_event)
        e.add('SUMMARY', self.subject_name)
        e.add('DESCRIPTION', f"Преподователь: {self.teacher}")
        e.add('LOCATION', self.place)
        e.add('LAST-MODIFIED', dt.datetime.now(self.tz))
        if self.repeat_type:
            e.add('RRULE',
                  {'freq': 'weekly', 'count': self.repeat_time, 'interval': 1 if self.repeat_type == 'weekly' else 2})
        return e
