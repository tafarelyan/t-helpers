from datetime import datetime


def time_difference(start_time, end_time):
    diff = str_to_datetime(end_time) - str_to_datetime(start_time)
    return '{0}:{1:02d}'.format(diff.seconds//3600, diff.seconds//60 % 60)


def str_to_datetime(time, fmt='%H:%M'):
    return datetime.strptime(time, fmt)


def datetime_to_str(time):
    return time.strftime('%H:%M')
