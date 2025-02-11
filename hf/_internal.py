def path_relative(path: str, /) -> str:
    path = path.replace("\\", "/")
    if "/" not in path:
        path = "./" + path
    return path