from dateutil.parser import parse
from traceback import format_exc
from datetime import datetime
from json import JSONEncoder


def valid_dt(date_string):
    validated_dt = None
    try:
        validated_dt = parse(date_string, ignoretz=True)
    except ValueError:
        pass
    return validated_dt


def call_back_handler(fn, exceptions, handler, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except exceptions:
        handler(fn)
        return fn(*args, **kwargs)
    except Exception:
        print(format_exc())


def valid_phone_number(mixed_string):
    only_digits = [ch for ch in str(mixed_string) if ch.isdigit()]
    try:
        return int(
            str(
                ''.join(
                    only_digits[1:]
                    if len(only_digits) > 7 and only_digits[0] == 1
                    else only_digits
                )
            )
        )
    except ValueError:
        return None


class DateTimeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
