from dataclasses import dataclass, KW_ONLY, field
from typing import Any, Type, Generic, TypeVar, Literal
import ncc as c
from datetime import datetime
import pandas as pd
import inspect
import os

_C_PREFIX = "prefix"
_C_MESSAGE = "message"
_C_ERROR_TYPE = "error_type"

@dataclass
class LoggerData:
    _: KW_ONLY
    error: Exception | None = None
    error_type: Type | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        if self.error:
            self.error_type = self.error.__class__

    def __str__(self) -> str:
        fields = []
        keys = self.fields_get()[2:]
        for k in keys:
            v = self.__dict__[k]
            if v is None: continue
            if isinstance(v, str):
                v = c.q(v)
            fields.append(f"{k}={v}")
        return ", ".join(fields)

    @classmethod
    def fields_get(self) -> str:
        args = inspect.getfullargspec(self.__init__)
        return [_C_PREFIX, _C_MESSAGE] + args.args[1:] + [_C_ERROR_TYPE] + args.kwonlyargs

T = TypeVar("T")

class Logger(Generic[T]):
    _EXT = ".csv"

    def __init__(self, name: str, dir: str, logger_data: Type[T], stdout_prefix: str | Literal[True] | None = None) -> None:
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

    def save(self, path: str | None = None) -> None:
        self.exported = True
        if path is None:
            path = f"{self.dir}/{self.name}{self._EXT}"
        header = not os.path.exists(path)
        self.df.to_csv(path, mode="a", encoding="utf-8", index=False, header=header)
        self._log("LOG SAVED", f"Log saved to {c.q(path)}", None, [c.green], True, True)

    def __del__(self) -> None:
        if self.exported: return
        self.warning(f"Log {c.q(self.name)} not saved to disk. Call .save() method", to_file=False)


@dataclass
class LD(LoggerData):
    abc: int
    _: KW_ONLY
    x: int | None = None
    y: str | None = None

l = Logger(__file__, ".", LD, c.italic("downloading"))

l.error("BAD", LD(123, y="HELLO", error=Exception("BAD THING")))

l.save()