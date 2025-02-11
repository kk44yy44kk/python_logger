from typing import Any

def json_find(json: dict | list | Any, ret: dict[str, Any]) -> None:
    """If `ret[some_key]` is a list it will be appended to"""
    if isinstance(json, dict):
        for k, v in json.items():
            if k in ret.keys():
                if isinstance(ret[k], list):
                    ret[k].append(v)
                else:
                    ret[k] = v
            else:
                json_find(v, ret)
    elif isinstance(json, list):
        for v in json:
            json_find(v, ret)