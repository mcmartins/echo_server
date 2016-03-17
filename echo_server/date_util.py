import datetime


def get_now():
    return datetime.datetime.now()


def difference_in_minutes(datetime1, datetime2):
    return difference_in_seconds(datetime1, datetime2) / 60


def difference_in_seconds(datetime1, datetime2):
    return (datetime2 - datetime1).seconds
