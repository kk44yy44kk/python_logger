from typing import Any, Generator, Callable, TypeVar, ParamSpec, Type
import pandas as pd

Row = list[Any]
ColumnInfo = tuple[Any, str, Any]
RowDict = dict[str, Any | Exception]

T = TypeVar("T")
P = ParamSpec("P")
PP = ParamSpec("PP")
BE = TypeVar("E", bound=BaseException)


def pcall(fun: Callable[P, T], *args: P.args, _pcall_type: Type[BE] | tuple[type[BE], ...] = Exception, **kwargs: P.kwargs) -> T | BE:
    try:
        return fun(*args, **kwargs)
    except _pcall_type as e:
        return e

def pcall_ignore(fun: Callable[P, T], *args: P.args, _pcall_type: Type[BaseException] | tuple[type[BaseException], ...] = Exception, **kwargs: P.kwargs) -> T | None:
    try:
        return fun(*args, **kwargs)
    except _pcall_type:
        return None


_ROW2DICT_ERRORS_IGNORE = (TypeError, ValueError, ZeroDivisionError)
def _row2dict(row: Row, keys: tuple[str | None, ...], key2fun: dict[str, Callable[[RowDict, str], Any]]) -> RowDict:
    d = {k: v for k, v in zip(keys, row) if k is not None}
    for k, fun in key2fun.items():
        d[k] = pcall_ignore(fun, d, k, _pcall_type=_ROW2DICT_ERRORS_IGNORE)
    return d


def rows2dicts(rows: list[Row], columns_info: list[ColumnInfo], column2key: dict[str, str] | None, key2fun: dict[str, Callable[[RowDict, str], Any]] = {}) -> Generator[RowDict, None, None]:
    """
    If `column2key` is `None`, names of db columns don't change.

    When a function in `key2fun` raises one of the exceptions from `_ROW2DICT_ERRORS_IGNORE`, it returns `None` instead
    """
    assert len(rows) == 0 or len(columns_info) == len(rows[0]), f"{len(columns_info)=} != {len(rows[0])=}"
    row_names: tuple[str | None, ...]
    if column2key is not None:
        row_names = tuple(map(lambda t: column2key.get(t[1], t[1]), columns_info))
        assert (x := set(row_names) - set(column2key.values())) == set(), f"Missing columns: {x}"
        assert (x := set(column2key.values()) - set(row_names)) == set(), f"Too many columns: {x}"
        assert len(row_names) == len(set(row_names)), f"Dupplicate row names in {row_names=}"
    else:
        row_names = tuple(map(lambda t: t[1], columns_info))
    return (_row2dict(row, row_names, key2fun) for row in rows)

def rows2df(mut_df: pd.DataFrame, i: int | None, rows: list[Row], columns_info: list[ColumnInfo], column2key: dict[str, str] | None, key2fun: dict[str, Callable[[RowDict, str], Any]] = {}) -> None:
    """See `rows2dicts`"""
    if i is None:
        i = len(mut_df.index)
    assert i >= 0
    dicts = rows2dicts(rows, columns_info, column2key, key2fun)
    for d in dicts:
        for k, v in d:
            mut_df.loc[i, k] = v
        i += 1

# rows = [
#     [100, "Bob", "Ross", 10],
#     [101, "Guy", "Guy", 25],
#     [102, "Aron", "Core", 43],
# ]

# columns_info = [
#     (1, "id", 1),
#     (1, "name", 1),
#     (1, "last", 1),
#     (1, "age", 1),
# ]

# # column2key = {
# #     "id": "id1",
# #     "name": "name1",
# #     "last": "last1",
# #     "age": "age1"
# # }

# column2key = None

# key2fun = {
#     # "age": lambda d, k: d[k] * 100,
#     "age+1": lambda d, k: 1 / 0,
#     "age+1+1": lambda d, k: d[1],
# }

# r = rows2dicts(rows, columns_info, column2key, key2fun)

# for d in r:
#     print(d)