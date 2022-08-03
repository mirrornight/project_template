import datetime
import calendar

from src.conf.config import TZ


def now_datetime():
    """获取实时datetime"""
    return datetime.datetime.now()


def now_tz_datetime():
    """获取带TIMEZONE的datetime"""
    return datetime.datetime.now(tz=TZ)


def now_tz_datestring(fmt: str = "%Y-%m-%d %H:%M:%S"):
    return strftime(now_tz_datetime(), fmt=fmt)


def init_datetime():
    """初始化数据时间"""
    return strptime("1970-01-01 00:00:00")


def strftime(date: datetime.datetime, fmt="%Y-%m-%d %H:%M:%S"):
    return date.strftime(fmt)


def strptime(datestr: str, fmt=None):
    if fmt is not None:
        return datetime.datetime.strptime(datestr, fmt)

    if len(datestr) == 10:
        return datetime.datetime.strptime(datestr, "%Y-%m-%d")
    elif len(datestr) == 19:
        return datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")


def days_date_range(start_date: datetime.datetime, end_date: datetime.datetime):
    """获取时间周期列表"""
    dates = []
    dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    date = start_date[:]
    while date <= end_date:
        dates.append(date)
        dt = dt + datetime.timedelta(days=1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def time_difference(date1: (str, datetime.datetime), date2: (str, datetime.datetime)):
    """获取时间差"""
    if isinstance(date1, str):
        date1 = strptime(date1)
    if isinstance(date2, str):
        date2 = strptime(date2)
    return date2 - date1


def convert_to_search_interval(start: (datetime.datetime, str), end: (datetime.datetime, str), length: int = 19):
    """
    转换%Y-%m-%d时间格式为%Y-%m-%d %H:%M:%S

    example:
        start: 2020-03-01将被转换为2020-03-01 00:00:00
        end: 2020-03-31将被转换为2020-03-31 23:59:59

    :param start: 起始时间
    :param end: 结束时间
    :param length: 时间长度
    :return: 起始和结束时间
    """
    start = convert_to_search_start_time(start)[:length]
    end = convert_to_search_end_time(end)[:length]
    return start, end


def convert_to_search_start_time(start: (datetime.datetime, str)):
    if isinstance(start, str) and len(start) == 19:
        return start

    if isinstance(start, datetime.datetime):
        start = start.date()
    elif isinstance(start, datetime.date):
        pass
    else:
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
    start = start.strftime("%Y-%m-%d %H:%M:%S")
    return start


def convert_to_search_end_time(end: (datetime.datetime, str)):
    if isinstance(end, str) and len(end) == 19:
        return end

    if isinstance(end, str):
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
    elif isinstance(end, datetime.date):
        end = datetime.datetime.combine(end, datetime.datetime.min.time())
    end = end.replace(hour=23, minute=59, second=59)

    end = end.strftime("%Y-%m-%d %H:%M:%S")
    return end


def get_month_range_date(year: int, month: int):
    weekday, month_end = calendar.monthrange(year=year, month=month)
    start = datetime.date(year=year, month=month, day=1)
    end = datetime.date(year=year, month=month, day=month_end)

    return start, end
