from bacon import settings


def is_odd(num):
    return num % 2


def error(key, **kwargs):
    return settings.ERRORS.get(key, '').format(**kwargs)