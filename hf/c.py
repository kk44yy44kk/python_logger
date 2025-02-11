# https://github.com/kk44yy44kk/ncc

from typing import Callable, Any, TypeVar, Iterable
from math import floor
from os import system

# Fix for windows consoles not rendering the text
system("")
print(end="")

ColorFun = Callable[[str], str]
"""It also has a `escape = True` keyword only argument"""
RGB = tuple[int, int, int]

def _make_color(code: int):
    def ret(text = "", *, escape = True) -> str:
        return f"\033[{code}m{text}\033[0m" if escape else f"\033[{code}m{text}"
    return ret

def compose(funcs: list[ColorFun]):
    """
    Composes many color function into one function
    """
    def ret(text: str, escape = True) -> str:
        for func in funcs:
            text = func(text, escape=escape)
        return text
    return ret

reset = _make_color(0)
"""Returns `text` with reset ANSI renditions. The `escape` argument does nothing and exists only to match other color functions' signatures."""
bold = _make_color(1)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
italic = _make_color(3)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
underline = _make_color(4)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
hide = _make_color(8)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
default = _make_color(39)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
black = _make_color(30)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
red = _make_color(31)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
green = _make_color(32)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
yellow = _make_color(33)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
blue = _make_color(34)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
magenta = _make_color(35)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
cyan = _make_color(36)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
white = _make_color(37)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
gray = _make_color(90)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
b_red = _make_color(91)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
b_green = _make_color(92)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
b_yellow = _make_color(93)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
b_blue = _make_color(94)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
b_magenta = _make_color(95)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
b_cyan = _make_color(96)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
b_white = _make_color(97)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_default = _make_color(39+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_black = _make_color(30+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_red = _make_color(31+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_green = _make_color(32+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_yellow = _make_color(33+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_blue = _make_color(34+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_magenta = _make_color(35+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_cyan = _make_color(36+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_white = _make_color(37+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_gray = _make_color(90+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_b_red = _make_color(91+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_b_green = _make_color(92+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_b_yellow = _make_color(93+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_b_blue = _make_color(94+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_b_magenta = _make_color(95+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_b_cyan = _make_color(96+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""
bg_b_white = _make_color(97+10)
"""Returns `text` renditioned with an ANSI code. If `escape` is `True`, the rendition will be reset at the end of the returned string."""

class Veil(list[ColorFun | Any]):
    """
    An object version of the `color` function. When it's converted to a string, all `ColorFun`s are ommited.
    In order to get get the color version, use it as an argument to the `color` function
    """
    def __init__(self, *args, sep=" ", escape=True) -> None:
        """
        An object version of the `color` function. When it's converted to a string, all `ColorFun`s are ommited.
        In order to get get the color version, use it as an argument to the `color` function
        """
        super().__init__(self)
        self.extend(args)
        self.sep: str = sep
        self.escape: bool = escape

    def __str__(self) -> str:
        return uncolor(self.sep.join(
            map(
                str,
                filter(lambda e: not isinstance(e, Callable), self)
            )
        ))

    def __repr__(self):
        return self.__str__()

def color(*args: any | ColorFun, escape = True, sep = " ") -> str:
    """
    Allows for chaining many `ColorFun`s without escaping them.

    `underline(cyan("Hello,", escape=False) + " " + magenta("World!"))`
    can be simplified into
    `color(underline, cyan, "Hello,", magenta, "World!")`
    """
    ret = ""
    for arg in args:
        if isinstance(arg, Callable):
            ret += arg(escape = False)
        elif isinstance(arg, Veil):
            ret += color(*arg, escape=arg.escape, sep=arg.sep) + sep
        else:
            ret += str(arg) + sep
    if ret.endswith(sep):
        ret = ret.removesuffix(sep)
    if escape:
        ret += reset()
    return ret.removesuffix(" ")

def highlight(text: str, sub: str, *, colors: list[ColorFun], colors2: list[ColorFun] = []) -> str:
    """
    Highlights every occurence of `sub` in `text` using `colors`. Unhighlighted parts get colored with `colors2`
    """
    ret = ""
    hl = compose(colors)
    hl2 = compose(colors2)
    i = 0
    i_prev = -99
    # Gaps are characters between islands of neighbouring subs
    gap_start = 0
    gap_end = 0
    while True:
        i = text.find(sub, i)
        if i == -1:
            break
        if i_prev != i - len(sub):
            ret += hl(text[gap_end:gap_start]) + hl2(text[gap_start:i])
            gap_end = i
        gap_start = i + len(sub)
        i_prev = i
        i += 1
    return ret + hl(text[gap_end:gap_start]) + hl2(text[gap_start:])

def highlight_range(text: str, start: int, stop: int, *, colors: list[ColorFun], colors2: list[ColorFun] = []) -> str:
    """
    Highlights `text` from `start` to `stop` using `colors`. Unhighlighted parts get colored with `colors2`

    Returns `text` if `start >= stop`. Throws an `AssertionError` if indexes are out of bounds
    """
    hl = compose(colors)
    hl2 = compose(colors2)
    if start >= stop:
        return text
    assert start >= 0 and start < len(text), f"Out of bounds start={start}"
    assert stop >= 0 and stop < len(text), f"Out of bounds stop={stop}"
    return hl2(text[:start]) + hl(text[start:stop]) + hl2(text[stop:])

def highlight_between(text: str, start: str, stop: str, *, colors: list[ColorFun], colors2: list[ColorFun] = []) -> str:
    """
    Highlights characters between every `start` and `stop` in `text` with `colors`. Unhighlighted parts get colored with `colors2`
    """
    i = 0
    hl = compose(colors)
    hl2 = compose(colors2)
    ret = ""
    while True:
        old_i = i
        i = text.find(start, i)
        j = text.find(stop, i + 1)
        if -1 in [i, j]:
            i = old_i
            break
        ret += hl2(text[old_i:i]) + hl(text[i:j+1])
        i = j + 1
    return ret + hl2(text[i:])

def uncolor(text: str) -> str:
    """
    Removes all ANSI graphical renditions
    """
    ret = ""
    start = 0
    stop = 0
    stop_old = 0
    while True:
        start = text.find("\033[", stop)
        stop_old = stop
        if start == -1:
            break
        ret += text[stop:start]
        # print(f"\"{text[stop:start]}\"", stop, start)
        stop = text.find("m", start) + 1
        if stop == 0:
            break

    return ret + text[stop_old:]

_PB_REPLACE = "$$"
_PB_REPLACE_PERCENT = "$%"
def bar(
        i: int, i_max: int, width: int, *,
        colors: list[ColorFun] = [green], colors2: list[ColorFun] = [white],
        chars = "=", chars2 = "-",
        frame_bar: str | None = f"[{_PB_REPLACE}]", frame_tail: str | None = _PB_REPLACE_PERCENT,
        head: str | None = None,
        on_complete: str | None = None,
    ) -> str:
    """
    TODO
    Returns a progress bar of a given `width`.

    `chars` are repeated for the completed part of the progress bar and are highlighted with `colors`. `chars2` and `colors2` work analogously.

    `frame_bar` is the string around the progress bar (not included in `width`), `"$$"` gets replaced with the progress bar itself.

    `frame_percentage` is the string around the progress percentage, `"$$"` gets replaced with the percentage. If you want to get rid of percentage set it to `""`.

    `head` replaces the last character in the repeated `chars`.

    `on_complete` replaces precentage and `frame_percentage` if `value == 1.0`.
    """
    value = float(i) / float(i_max)
    # TODO?: make gradients scale properly
    # TODO:  head at 0 progress width should be 0 % or sth
    assert chars != "" and chars2 != "", "Chars can't be empty strings"
    hl = compose(colors)
    hl2 = compose(colors2)
    tail_label = ""
    if on_complete is not None and value == 1:
        tail_label = " " + on_complete
    elif frame_tail is not None:
        tail_label = " " + frame_tail
        if _PB_REPLACE_PERCENT in frame_tail:
            digits = int(value * 100)
            tail_label = tail_label.replace(_PB_REPLACE_PERCENT, f"{digits}%")
            tail_label += " " * (3 - len(str(digits)))
        if _PB_REPLACE in frame_tail:
            tail_label = tail_label.replace(_PB_REPLACE, f"{i}/{i_max}")
            tail_label += " " * max(0, len(str(i_max)) - len(str(i)))
    progress_width = floor(min(1.0, value) * width)
    progress = (chars * width)[:progress_width]
    if head is not None:
        assert len(head) == 1, f"progress_head=\"{head}\", it needs to be 1 character long"
        progress = progress[:-1] + head
    background = (chars2 * width)[progress_width:width]
    body = f"{hl(progress)}{hl2(background)}"
    body = frame_bar.replace(_PB_REPLACE, body)
    return f"{body}{tail_label}"

T = TypeVar("T")
class ProgressBar:
    def __init__(self, progress_bar: Callable[[int, int], None]):
        self.progress_bar = progress_bar
        self.pb = ""

    def __call__(self, iter: Iterable[T]):
        self.iterating = True
        i_max = max(1, len(iter))
        print(self.progress_bar(0, i_max) + "\033[F")
        for i, element in enumerate(iter):
            self.pb = self.progress_bar(i, i_max)
            print(self.pb + "\033[F")
            yield element
        print(self.progress_bar(i_max, i_max) + "\n\033[K\033[F")

    def print(self, *args, **kwargs) -> None:
        text = "\033[K\033[F\033[K"
        text += kwargs.get("sep", " ").join(map(str, args)) + "\n" + self.pb + "\033[F\n"
        print(text, **kwargs)

_d, _n, _l = 90, 180, 255
approx_colors: tuple[RGB, ColorFun, ColorFun] = [
    ((0, 0, 0), black, bg_black),
    ((_n, 0, 0), red, bg_red),
    ((0, _n, 0), green, bg_green),
    ((_n, _d, 0), yellow, bg_yellow),
    ((0, 0, _n), blue, bg_blue),
    ((_n, 0, _n), magenta, bg_magenta),
    ((0, _n, _n), cyan, bg_cyan),
    ((_n, _n, _n), white, bg_white),
    ((_l, _d, _d), b_red, bg_b_red),
    ((_d, _l, _d), b_green, bg_b_green),
    ((_l, _l, _d), b_yellow, bg_b_yellow),
    ((_d, _d, _l), b_blue, bg_b_blue),
    ((_l, _d, _l), b_magenta, bg_b_magenta),
    ((_d, _l, _l), b_cyan, bg_b_cyan),
    ((_l, _l, _l), b_white, bg_b_white),
    ((_d, _d, _d), gray, bg_gray),
]
"""Used for approximating colors. Don't set it directly, use `approx_colors_set`"""

_color2approx: dict[ColorFun, RGB]

def approx_colors_set(new: tuple[RGB, ColorFun, ColorFun]) -> None:
    global approx_colors
    global _color2approx
    approx_colors = new
    _color2approx = {fn: rgb for rgb, fn, bg_fn in approx_colors}
    _color2approx.update({bg_fn: rgb for rgb, fn, bg_fn in approx_colors})

approx_colors_set(approx_colors)

def _approx_color_i_get(r: int, g: int, b: int) -> int:
    minimum = 256*3
    minimum_i = -1
    for i, clr in enumerate(approx_colors):
        r2, g2, b2 = clr[0]
        diff = abs(r2 - r) + abs(g2 - g) + abs(b2 - b)
        if diff < minimum:
            minimum = diff
            minimum_i = i
    return minimum_i

approx_colors_force = False

def approx_colors_force_set(value: bool) -> None:
    """
    If `approx_colors_force` is `True`, then functions `rgb` and `bg_rgb` will return the closest predefined color functions based on `approx_colors`.

    Ex. `rgb(0, 0, 0)` should return the `black` function.
    """
    global approx_colors_force
    approx_colors_force = value

def rgb(r: int, g: int, b: int):
    """
    Returns a custom 24-bit color function
    """
    assert r in range(256), f"r = {r}, it needs to be in range 0..255"
    assert g in range(256), f"g = {g}, it needs to be in range 0..255"
    assert b in range(256), f"b = {b}, it needs to be in range 0..255"
    global approx_colors_force
    if approx_colors_force:
        i = _approx_color_i_get(r, g, b)
        return approx_colors[i][1]
    def ret(txt: str, escape = True) -> str:
        return f"\033[38;2;{r};{g};{b}m{txt}\033[0m" if escape else f"\033[38;2;{r};{g};{b}m{txt}"
    return ret

def bg_rgb(r: int, g: int, b: int):
    """
    Returns a custom 24-bit color function for backgrounds
    """
    assert r in range(256), f"r = {r}, it needs to be in range 0..255"
    assert g in range(256), f"g = {g}, it needs to be in range 0..255"
    assert b in range(256), f"b = {b}, it needs to be in range 0..255"
    global approx_colors_force
    if approx_colors_force:
        i = _approx_color_i_get(r, g, b)
        return approx_colors[i][2]
    def ret(txt: str, escape = True) -> str:
        return f"\033[48;2;{r};{g};{b}m{txt}\033[0m" if escape else f"\033[48;2;{r};{g};{b}m{txt}"
    return ret


def _make_gradient_rgb(rgb_fn: Callable):
    assert rgb_fn in [rgb, bg_rgb], "It needs to be one of these two functions"
    def gradient_rgb(start: RGB, stop: RGB):
        def ret(text = "", escape = True) -> str:
            ret = ""
            rgb = start
            if text != "":
                fraction = 1 / len(text)
            for char in text:
                rgb = (
                    rgb[0] + (fraction) * (stop[0] - start[0]),
                    rgb[1] + (fraction) * (stop[1] - start[1]),
                    rgb[2] + (fraction) * (stop[2] - start[2]),
                )
                ret += rgb_fn(int(rgb[0]), int(rgb[1]), int(rgb[2]))(char, escape=False)
            if escape:
                ret += reset()
            return ret
        return ret
    return gradient_rgb

gradient_rgb = _make_gradient_rgb(rgb)
"""Returns an RGB gradient function from `start` to `stop`"""
bg_gradient_rgb = _make_gradient_rgb(bg_rgb)
"""Returns an RGB background gradient function from `start` to `stop`"""

def gradient(start: ColorFun, stop: ColorFun):
    """
    Returns an approximate gradient function from `start` to `stop`. Approximations are based on `approx_colors`
    """
    assert start in _color2approx.keys(), "This function only accepts premade color functions like red or bg_cyan"
    assert stop in _color2approx.keys(), "This function only accepts premade color functions like red or bg_cyan"
    return gradient_rgb(_color2approx[start], _color2approx[stop])

def bg_gradient(start: ColorFun, stop: ColorFun):
    """
    Returns an approximate background gradient function from `start` to `stop`. Approximations are based on `approx_colors`
    """
    assert start in _color2approx.keys(), "This function only accepts premade color functions like red or bg_cyan"
    assert stop in _color2approx.keys(), "This function only accepts premade color functions like red or bg_cyan"
    return bg_gradient_rgb(_color2approx[start], _color2approx[stop])

def hex2rgb(code: str) -> RGB:
    """
    Converts color hex into an RGB tuple.Examples:

    `"#00FF00"` -> `(0, 255, 0)`,

    `"000000"` -> `(0, 0, 0)`

    """
    code = code.removeprefix("#")
    assert len(code) == 6, "TODO"
    return (int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16))

def q(text: Any, qm = "\"", colors: list[ColorFun] = [], colors_text: list[ColorFun] = []) -> str:
    hl = compose(colors)
    hl_text = compose(colors_text)
    return hl(qm + hl_text(str(text)) + hl(qm))
