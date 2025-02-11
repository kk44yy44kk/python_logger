from typing import Any, TypeVar

T = TypeVar("T")

Error = tuple[Any, ...]
"""
First element should be a string
"""

Result = tuple[T | None, tuple[Any, ...] | None]
"""
For Go-like error handling
```
val, err = some_function() # function that returns a Result
if err is not None:
    print("Error:", error_str(err))
else:
    print("Result:", val)
```
"""

def ok(value: T) -> Result[T]:
    return value, None

def error(*error: Any) -> Result[Any]:
    assert len(error) != 0, f"No error message in {error=}"
    assert isinstance(error[0], str), f"First element in {error=} needst to be a str"
    return None, error

def error_from_exception(e: BaseException) -> Error:
    return(e.__class__.__name__, str(e), )

def error_str(error: Error) -> str:
    """
    Formats `error` as a `str`
    """
    assert len(error) != 0, f"No error message in {error=}"
    msg = error[0]
    assert isinstance(msg, str), f"First element in {error=} needst to be a str"
    if len(error) == 1:
        return msg
    over = len(error) - 1 - msg.count("{")
    assert msg.count("{") == msg.count("}"), f"Different number of \"{{\" and \"}}\" in {error=}"
    assert over > 0, f"To many \"{{}}\" in {error=}"
    msg = msg.format(*error[1:])
    if over > 0:
        msg += ": " + ", ".join(map(str, error[-over:]))
    return msg
