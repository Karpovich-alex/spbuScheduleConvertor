from icalendar import Calendar, Event
import pandas as pd
import datetime as dt
import pytz
from examples.event_example import event

cal = Calendar()
cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')


class Subject:
    params = ['TimeStart', 'TimeEnd', 'DateStart', 'DateEnd', 'SubjectName', 'Place', 'Teacher', 'RepeatTime', 'SubGroup']
    tz = pytz.timezone('Europe/Moscow')

    def __init__(self, TimeStart, TimeEnd, DateStart, DateEnd, SubjectName, Place, Teacher, RepeatTime=1, SubGroup=None):
        self.time_start = TimeStart
        self.time_end = TimeEnd
        self.date_start = DateStart
        self.date_end = DateEnd
        self.subject_name = SubjectName
        self.place = Place
        self.teacher = Teacher
        self.repeat_time = RepeatTime
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
        return f"<Subject time start: {self.time_start} date start: {self.date_start} with {self.repeat_time} repeats>"

    def to_event(self) -> Event:
        e = Event()
        e.add('DTSTART', self.date_time_start_event)
        e.add('DTEND', self.date_time_end_event)
        e.add('SUMMARY', self.subject_name)
        e.add('DESCRIPTION', f"Преподователь: {self.teacher}")
        e.add('LOCATION', self.place)
        e.add('LAST-MODIFIED', dt.datetime.now(self.tz))
        e.add('RRULE', {'freq': 'weekly', 'count': self.repeat_time})
        return e


df = pd.read_csv('autumn.csv')

df['DateStart'] = pd.to_datetime(df['DateStart'])
df['DateEnd'] = pd.to_datetime(df['DateEnd'])
df['TimeStart'] = pd.to_datetime(df['TimeStart'])
df['TimeEnd'] = pd.to_datetime(df['TimeEnd'])
for idx, item in df.iterrows():
    item.TimeStart = pd.to_datetime(item.TimeStart, format='%H:%M:%S').time()
    item.TimeEnd = pd.to_datetime(item.TimeEnd, format='%H:%M:%S').time()
    item.DateStart = pd.to_datetime(item.DateStart, format='%d.%m.%Y')
    item.DateEnd = pd.to_datetime(item.DateEnd, format='%d.%m.%Y')
    s = Subject.from_series(item)

    e = s.to_event()
    cal.add_component(e)

with open('example_autumn.ics', 'wb') as f:
    f.write(cal.to_ical())
