from typing import Callable, Any, Type, TypeVar
import inspect
import sys



class CLIError(Exception):
    pass

class ParsingError(CLIError):
    pass


def good_constr(t: Type) -> bool:
    return callable(t)


FORBIDDEN_KWARGS = ["return"]


def s(a):
    if isinstance(a, str):
        return f"\"{a}\""
    else:
        return str(a)

def argv_parse(cli_argv: list[str], argspec: inspect.FullArgSpec, *, allow_duplicates = False, allow_empty_values = False) -> tuple[list[str], dict[str, str]]:
    args: list[str] = []
    kwargs: dict[str, str] = {}

    last_long: str | None = None
    for arg in cli_argv[1:]:
        if arg == "--":
            raise ParsingError("Arg -- ????")

        if last_long is not None:
            if not allow_duplicates and kwargs.get(last_long) is not None:
                raise ParsingError("TODO dup 0")
            kwargs[last_long] = arg
            last_long = None
        elif arg.startswith("--"):
            long = arg.split("=")[0].removeprefix("--")
            if long in FORBIDDEN_KWARGS:
                raise ParsingError(f"Forbinden keyword \"{long}\"")
            if "=" in arg:
                v = "=".join(arg.split("=")[1:])
                if not allow_empty_values and v == "":
                    raise ParsingError("TODO empty")
                if not allow_duplicates and kwargs.get(long) is not None:
                    raise ParsingError("TODO duplicate")
                kwargs[long] = v
            else:
                last_long = long
        else:
            args.append(arg)

    if not allow_duplicates:
        for name in kwargs.keys():
            if name not in argspec.args: continue
            print(f"{argspec.args.index(name)=}")
            if len(args) <= argspec.args.index(name): continue
            raise CLIError("CROSSKWDLICATE")

    if last_long is not None:
        raise CLIError("NO VALUE KWARG")

    return (args, kwargs,)

def args_constructors(fn: Callable, argspec: inspect.FullArgSpec) -> dict[int | str | Callable[[str], Any]]:
    # TODO: get type from default if no annotation
    # TODO: bool flags
    ret: dict[int | str | Callable[[str], Any]] = {}
    for i, arg in enumerate(argspec.args):
        type = argspec.annotations.get(arg, None)
        if argspec.defaults and i >= len(argspec.args) - len(argspec.defaults):
            type_default = argspec.defaults[i - len(argspec.defaults) - 1].__class__
            if type != type_default:
                if type is None:
                    type = type_default
                else:
                    raise CLIError("x: int = 'hello'")
        else:
            type = str

        if not good_constr(type):
            raise CLIError("TODO BAD CPMST")
        ret[arg] = type
        ret[i] = type

    additional = [argspec.varargs, argspec.varkw]
    for kwarg in argspec.kwonlyargs + [name for name in additional if name is not None]:
        type = argspec.annotations.get(kwarg, None)
        if argspec.kwonlydefaults and argspec.kwonlydefaults.get(kwarg):
            type_default = argspec.kwonlydefaults[kwarg].__class__
            if type != type_default:
                if type is None:
                    type = type_default
                else:
                    raise CLIError("*x: int = 'hello'")
            else:
                type = str

        if not good_constr(type):
            if kwarg in additional:
                type = str
            else:
                raise CLIError(f"TODO BAD {kwarg=} CPMST {type=}")
        ret[kwarg] = type

    return ret

# TODO: list constructor
# TODO: fn def error

def args_auto_help(name: str, desc: str, argspec: inspect.FullArgSpec, constructors: dict[str, Callable]) -> str:
    TAB = "\t"
    ret = ""
    ret += "NAME"
    ret += f"\n{TAB}{name} " + f"\n{TAB}".join(map(str.strip, desc.split("\n")))
    ret += "\n\nUSAGE"
    ret += f"\n{TAB}{name}"

    skip = [
        argspec.varkw,
        argspec.varargs,
    ]
    kewords_len = len(argspec.args) + len(argspec.kwonlyargs)
    # if argspec.varkw:
    #     kewords_len += 2
    if kewords_len > 0:
        if kewords_len == 1:
            ret += " [option]"
        else:
            ret += " [option...]"
    if argspec.varkw:
        type = constructors[argspec.varkw].__name__.upper()
        ret += f" [variadic_option={type}...]"
    args_len = len(argspec.args)
    # if argspec.varargs:
    #     args_len += 2
    if args_len > 0:
        if args_len == 1:
            ret += " [operand]"
        else:
            ret += " [operands...]"
    if argspec.varargs:
        type = constructors[argspec.varargs].__name__.upper()
        ret += f" [variadic_operand={type}...]"
    # TODO: literals
    ret += f"\n{TAB}{name} --help"
    ret += "\n\nOPTIONS"
    default_operand_i = len(argspec.args) - (len(argspec.defaults) if argspec.defaults else 0)
    print(f"{default_operand_i=}")
    i = 0
    for name, constructor in constructors.items():
        if isinstance(name, int) or name in skip:
            continue
        ret += f"\n{TAB}"
        if name in argspec.args:
            ret += f"operand {i}, "
        ret += f"--{name}"
        ret += f"={constructor.__name__.upper()}"
        if name in argspec.args:
            # ret += f"\n{TAB}{TAB}operand index: {argspec.args.index(name)}"
            if i >= default_operand_i:
                value = argspec.defaults[default_operand_i - i]
                ret += f"\n{TAB}{TAB}default: {s(value)}"
            i += 1
        if argspec.kwonlydefaults and argspec.kwonlydefaults.get(name):
            ret += f"\n{TAB}{TAB}default: {s(argspec.kwonlydefaults[name])}"
    return ret
# TODO: "--"



T = TypeVar("T")
def args_call(fn: Callable[..., T], argv: list[str], *, allow_duplicates = False, allow_empty_values = False, auto_generate_help = True) -> T:
    # TODO: options before operands
    argspec = inspect.getfullargspec(fn)
    constructors = args_constructors(fn, argspec)
    # TODO: check if argv have valid args
    if "--help" in argv:
        name = argv[0].replace("\\", "/").split("/")[-1]
        desc = f"- {fn.__doc__.strip()}" if fn.__doc__ else ""
        return args_auto_help(name, desc, argspec, constructors)

    raw_args, raw_kwargs = argv_parse(argv, argspec, allow_duplicates=allow_duplicates, allow_empty_values=allow_empty_values)
    args: list[Any] = []
    if argspec.varargs is None and len(raw_args) > len(argspec.args):
        raise CLIError("TOO MANY ARGS")
    args_constructor = constructors.get(argspec.varargs)
    for i, value in enumerate(raw_args):
        args.append(constructors.get(i, args_constructor)(value))
    kwargs: dict[str, Any] = {}
    kwargs_constructor = constructors.get(argspec.varkw)
    for name, value in raw_kwargs.items():
        type = constructors.get(name, kwargs_constructor)
        if type is None:
            raise CLIError(f"NO KWARGS??? {argspec.varkw=} {kwargs_constructor=}")
        kwargs[name] = type(value)

    print(constructors)
    # print(args, kwargs)
    return fn(*args, **kwargs)



def cat(*args, sep: str) -> str:
    """
    a program that returns
    your what you put inside of it
    """
    return sep.join(args)


print(
    args_call(cat, sys.argv)
)
