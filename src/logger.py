from typing import Any


class Logger:
    def __init__(self, function) -> None:
        self.function = function

    def __call__(self, *args, **kwargs) -> None:
        try:
            result = self.function(*args, **kwargs)
            self._log_output(result, "log.txt")
        except Exception as e:
            self._log_output(e, "crash_log.txt")
            raise

    def _log_output(self, output: Any, filename: str) -> None:
        with open(filename, "a") as log_file:
            log_file.write(str(output) + "\n")


@Logger
def log_exception(exception: Exception) -> None:
    raise exception


@Logger
def log_string(string: str) -> str:
    return string


@Logger
def log_iterable(iterable: list | tuple, name: str = "Array") -> str:
    string = name + ":\n"
    for i in iterable:
        string += "\t" + str(i)
    return string + "\n"


@Logger
def log_dict(json: dict, name: str = "json") -> str:
    def pprint_json(json: dict | list) -> str:
        if isinstance(json, dict):
            string = "{\n"
            for key, value in json:
                if not isinstance(value, dict):
                    string += f"\t{key}: {value}\n"
                else:
                    string += f"\t{key}: {pprint_json(value)}\n"
            string += "}"
        elif isinstance(json, list):
            string = "[\n"
            for i in json:
                string += f"\t{i},\n"
            string = "]"
        return string

    string = name + ":\n"
    string += pprint_json(json=json)
    return string


@Logger
def log_object(obj: object) -> str:
    return str(obj)
