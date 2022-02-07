import aiohttp
import aiofiles
import asyncio
import datetime

group_id = 304456
url = "https://timetable.spbu.ru/StudentGroupEvents/ExcelWeek?studentGroupId={group_id}&weekMonday={week}".format(
    group_id=group_id)  # yyyy-mm-dd
start_date = datetime.date(2022, 2, 7)
end_date = datetime.date(2022, 6, 6)


async def get_excel(session, date):
    excel_url = url.format(week=date.isoformat())
    async with session.get(excel_url) as resp:
        if resp.status == 200:
            f = await aiofiles.open(f'./excels/{date.isoformat()}.xlsx', mode='wb')
            await f.write(await resp.read())
            await f.close()


def get_dates():
    date = start_date
    while date <= end_date:
        yield date
        date = date + datetime.timedelta(days=7)


async def main():
    headers = {"Accept-Language": "ru-RU,ru;q=0.9"}
    async with aiohttp.ClientSession(headers=headers) as session:
        for date in get_dates():
            await get_excel(session, date)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# asyncio.run(main())
