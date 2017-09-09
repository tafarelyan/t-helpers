import datetime as dt


def time_difference(start_time, end_time):
    diff = time_str2datetime(end_time) - time_str2datetime(start_time)
    return '{0}:{1:02d}'.format(diff.seconds//3600, diff.seconds//60 % 60)


def time_str_to_datetime(time, fmt='%H:%M'):
    return dt.datetime.strptime(time, fmt)


def datetime_to_time_str(time):
    return time.strftime('%H:%M')
