import sys
from typing import Any


class Logger:
    def __init__(self, function) -> None:
        self.function = function

    def __call__(self, output: Any | Exception) -> None:
        if isinstance(output, Exception):
            with open("crash_log.txt", "a") as sys.stderr:
                self.function(output)
                print()
        else:
            with open("log.txt", "a") as sys.stdout:
                self.function(output)
                print()


@Logger
def log_exception(exception: Exception) -> None:
    raise exception


@Logger
def log_string(string: str) -> None:
    print(string)


@Logger
def log_iterable(iterable: list | tuple, name: str = "Array") -> None:
    print(name + ":")
    for i in iterable:
        print("/t" + i)


@Logger
def log_dict(json: dict, name: str = "json") -> None:
    print(name + ":")
    from pprint import pp

    pp(json)


@Logger
def log_object(obj: object) -> None:
    print(obj)
