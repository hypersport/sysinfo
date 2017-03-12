from datetime import datetime


def format_time(value, date_format='%Y-%m-%d %H:%M:%S'):
    dt = datetime.fromtimestamp(int(value))
    return dt.strftime(date_format)
