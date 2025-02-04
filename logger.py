# https://github.com/kk44yy44kk/python_logger

from dataclasses import dataclass, KW_ONLY
from typing import Any, Type, Generic, TypeVar, Literal, Callable
import ncc as c
from datetime import datetime
import pandas as pd
import inspect
import os
import shared

# Columns
_C_TIME_STAMP = "time_stamp"
_C_PREFIX = "prefix"
_C_MESSAGE = "message"
_C_ERROR = "error"

def _exception2str(e: BaseException, qm: str = "\"") -> str:
    return f"{e.__class__.__name__}: {c.q(e, qm)}"

@dataclass
class LoggerData:
    _: KW_ONLY
    error: Exception | None = None

    def __str__(self) -> str:
        fields = []
        keys = self.fields_get()[3:]
        for k in keys:
            v = self.__dict__[k]
            if v is None:
                continue
            elif isinstance(v, str):
                v = c.q(v)
            elif isinstance(v, BaseException):
                v = _exception2str(v)
            fields.append(f"{k}={v}")
        return ", ".join(fields)

    @classmethod
    def fields_get(self) -> str:
        args = inspect.getfullargspec(self.__init__)
        return [_C_TIME_STAMP, _C_PREFIX, _C_MESSAGE] + args.args[1:] + args.kwonlyargs

T = TypeVar("T")

class Logger(Generic[T]):
    _EXT = ".csv"

    def __init__(self, name: str, dir: str, logger_data: Type[T], stdout_prefix: str | Literal[True] | None = None, append = True) -> None:
        """If `append` is `True`, log file will be appended, else a new log file will be created with a name `f"{name}-{n}"`"""
        name = name.replace("\\", "/")
        if "/" in name:
            name = name.split("/")[-1]
        self.name = name
        self.dir = dir.replace("\\", "/").rstrip("/")
        columns = logger_data.fields_get()
        self.df = pd.DataFrame(columns=columns)
        self.exported = False
        self.prefix: str | None
        if stdout_prefix is True:
            self.prefix = self.name
        else:
            self.prefix = stdout_prefix
        self.append = append
        self.print = print

    def _log(self, prefix: str, message: Any, data: T | None, prefix_colors: list[c.ColorFun], to_stdout: str, to_file: bool) -> None:
        if to_stdout:
            log_stdout = f"{c.compose(prefix_colors)(prefix)}: {message}"
            if self.prefix is not None:
                log_stdout = f"{self.prefix} {log_stdout}"
            if data is not None:
                log_stdout += ". " + str(data)
            self.print(log_stdout)
        if to_file:
            dic = data.__dict__ if data is not None else {}
            dic.update({
                _C_TIME_STAMP: datetime.now(),
                _C_PREFIX: prefix,
                _C_MESSAGE: message
            })
            df_i = len(self.df.index)
            for k, v in dic.items():
                if k.startswith("__") or v is None:
                    continue
                self.df.loc[df_i, k] = v

    def error(self, message: Any, data: T | None = None, *, to_stdout = True, to_file = True) -> None:
        self._log("ERROR", message, data, [c.red], to_stdout, to_file)

    def warning(self, message: Any, data: T | None = None, *, to_stdout = True, to_file = True) -> None:
        self._log("WARNING", message, data, [c.yellow], to_stdout, to_file)

    def info(self, message: Any, data: T | None = None, *, to_stdout = True, to_file = True) -> None:
        self._log("INFO", message, data, [c.gray], to_stdout, to_file)

    def success(self, message: Any, data: T | None = None, *, to_stdout = True, to_file = True) -> None:
        self._log("SUCCESS", message, data, [c.green], to_stdout, to_file)

    def debug(self, message: Any, data: T | None = None, *, to_stdout = True, to_file = True) -> None:
        self._log("DEBUG", message, data, [c.magenta], to_stdout, to_file)

    def save(self, path: str | None = None) -> str:
        # TODO: normalise path
        # TODO: assert if columns have changed
        self.exported = True
        ext = self._EXT
        if path is None:
            path = f"{self.dir}/{self.name}{self._EXT}"
        else:
            ext = "." + path.split(".")[-1]
        path = shared.path_relative(path)

        dir = "/".join(path.split("/")[:-1])
        # TODO: assert exists dir
        name_f = path.split("/")[-1].removesuffix(ext)
        header: bool
        if self.append:
            header = not os.path.exists(path)
        else:
            header = True
            n = 1
            for name in os.listdir(dir):
                if not name.startswith(name_f):
                    continue
                number = name.removeprefix(name_f + "-").removesuffix(ext)
                if number.isdigit():
                    n = max(n, int(number) + 1)
            path = f"{dir}/{name_f}-{n}{ext}"
        action = "saved" if header else "appended"
        df = self.df.copy()
        df[_C_ERROR] = df[_C_ERROR].map(lambda e: _exception2str(e, ""))
        df.to_csv(path, mode="a", encoding="utf-8", index=False, header=header)
        self._log("LOG SAVED", f"Log {action} to {c.q(path)}", None, [c.green], True, True)
        return path

    def __del__(self) -> None:
        if self.exported:
            return
        self.warning(f"Log {c.q(self.name)} not saved to disk. Call .save() method", to_file=False)
