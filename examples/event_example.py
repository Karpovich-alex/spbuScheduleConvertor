import pandas as pd
event = pd.read_json(
    '{"Time":"13:15\\u201314:45","Date":"12.02\\u201330.04 (12)","SubjectName":"\\u0412\\u044b\\u0447\\u0438\\u0441\\u043b\\u0438\\u0442\\u0435\\u043b\\u044c\\u043d\\u044b\\u0435 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u044b, \\u0441\\u0435\\u0442\\u0438 \\u0438 \\u0442\\u0435\\u043b\\u0435\\u043a\\u043e\\u043c\\u043c\\u0443\\u043d\\u0438\\u043a\\u0430\\u0446\\u0438\\u0438, \\u043a\\u043e\\u043d\\u0442\\u0440\\u043e\\u043b\\u044c\\u043d\\u0430\\u044f \\u0440\\u0430\\u0431\\u043e\\u0442\\u0430","Place":"\\u0421 \\u0438\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435\\u043c \\u0438\\u043d\\u0444\\u043e\\u0440\\u043c\\u0430\\u0446\\u0438\\u043e\\u043d\\u043d\\u043e-\\u043a\\u043e\\u043c\\u043c\\u0443\\u043d\\u0438\\u043a\\u0430\\u0446\\u0438\\u043e\\u043d\\u043d\\u044b\\u0445 \\u0442\\u0435\\u0445\\u043d\\u043e\\u043b\\u043e\\u0433\\u0438\\u0439","Teacher":"\\u042e\\u0440\\u043a\\u043e\\u0432 \\u0410. \\u0412.","DateStart":"12.02.2021","DateEnd":"30.04.2021","RepeatTime":"12","SubGroup":"\\u041f\\u043e\\u0434\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430 2","TimeStart":"13:15:00","TimeEnd":"14:45:00"}',
    orient='index')
event = event[0]
event.TimeStart = pd.to_datetime(event.TimeStart, format='%H:%M:%S').time()
event.TimeEnd = pd.to_datetime(event.TimeEnd, format='%H:%M:%S').time()
event.DateStart = pd.to_datetime(event.DateStart, format='%d.%m.%Y')
event.DateEnd = pd.to_datetime(event.DateEnd, format='%d.%m.%Y')