# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file implements an expression syntax, similar to ``printf``, for adding
ANSI colors to text.

See :func:`colorize`, :func:`cwrite`, and :func:`cprint` for routines that can
generate colored output.

:func:`colorize` will take a string and replace all color expressions with
ANSI control codes.  If the ``isatty`` keyword arg is set to False, then
the color expressions will be converted to null strings, and the
returned string will have no color.

:func:`cwrite` and :func:`cprint` are equivalent to ``write()`` and ``print()``
calls in python, but they colorize their output.  If the ``stream`` argument is
not supplied, they write to ``sys.stdout``.

Here are some example color expressions:

==============  ============================================================
Expression      Meaning
==============  ============================================================
``@r``          Turn on red coloring
``@R``          Turn on bright red coloring
``@*{foo}``     Bold foo, but don't change text color
``@_{bar}``     Underline bar, but don't change text color
``@*b``         Turn on bold, blue text
``@_B``         Turn on bright blue text with an underline
``@.``          Revert to plain formatting
``@*g{green}``  Print out 'green' in bold, green text, then reset to plain.
``@*ggreen@.``  Print out 'green' in bold, green text, then reset to plain.
==============  ============================================================

The syntax consists of:

==========  =====================================================
color-expr  ``'@' [style] color-code '{' text '}' | '@.' | '@@'``
style       ``'*' | '_'``
color-code  ``[krgybmcwKRGYBMCW]``
text        ``.*``
==========  =====================================================

``@`` indicates the start of a color expression.  It can be followed
by an optional ``*`` or ``_`` that indicates whether the font should be bold or
underlined.  If ``*`` or ``_`` is not provided, the text will be plain.  Then
an optional color code is supplied.  This can be ``[krgybmcw]`` or ``[KRGYBMCW]``,
where the letters map to  ``black(k)``, ``red(r)``, ``green(g)``, ``yellow(y)``, ``blue(b)``,
``magenta(m)``, ``cyan(c)``, and ``white(w)``.  Lowercase letters denote normal ANSI
colors and capital letters denote bright ANSI colors.

Finally, the color expression can be followed by text enclosed in ``{}``.  If
braces are present, only the text in braces is colored.  If the braces are
NOT present, then just the control codes to enable the color will be output.
The console can be reset later to plain text with ``@.``.

To output an ``@``, use ``@@``.  To output a ``}`` inside braces, use ``}}``.
"""
import io
import os
import re
import sys
import textwrap
from contextlib import contextmanager
from typing import Iterator, List, NamedTuple, Optional, Tuple, Union


class ColorParseError(Exception):
    """Raised when a color format fails to parse."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


# Text styles for ansi codes
styles = {"*": "1", "_": "4", None: "0"}  # bold  # underline  # plain

# Dim and bright ansi colors
colors = {
    "k": 30,
    "K": 90,  # black
    "r": 31,
    "R": 91,  # red
    "g": 32,
    "G": 92,  # green
    "y": 33,
    "Y": 93,  # yellow
    "b": 34,
    "B": 94,  # blue
    "m": 35,
    "M": 95,  # magenta
    "c": 36,
    "C": 96,  # cyan
    "w": 37,
    "W": 97,
}  # white

# Regex to be used for color formatting
COLOR_RE = re.compile(r"@(?:(@)|(\.)|([*_])?([a-zA-Z])?(?:{((?:[^}]|}})*)})?)")

# Mapping from color arguments to values for tty.set_color
color_when_values = {"always": True, "auto": None, "never": False}


def _color_when_value(when: Union[str, bool, None]) -> Optional[bool]:
    """Raise a ValueError for an invalid color setting.

    Valid values are 'always', 'never', and 'auto', or equivalently,
    True, False, and None.
    """
    if isinstance(when, bool) or when is None:
        return when

    elif when not in color_when_values:
        raise ValueError(f"Invalid color setting: {when}")

    return color_when_values[when]


def _color_from_environ() -> Optional[bool]:
    try:
        return _color_when_value(os.environ.get("SPACK_COLOR", "auto"))
    except ValueError:
        return None


#: When `None` colorize when stdout is tty, when `True` or `False` always or never colorize resp.
_force_color = _color_from_environ()


def try_enable_terminal_color_on_windows() -> None:
    """Turns coloring in Windows terminal by enabling VTP in Windows consoles (CMD/PWSH/CONHOST)
    Method based on the link below
    https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences#example-of-enabling-virtual-terminal-processing

    Note: No-op on non windows platforms
    """
    if sys.platform == "win32":
        import ctypes
        import msvcrt
        from ctypes import wintypes

        try:
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            DISABLE_NEWLINE_AUTO_RETURN = 0x0008
            kernel32 = ctypes.WinDLL("kernel32")

            def _err_check(result, func, args):
                if not result:
                    raise ctypes.WinError(ctypes.get_last_error())
                return args

            kernel32.GetConsoleMode.errcheck = _err_check
            kernel32.GetConsoleMode.argtypes = (
                wintypes.HANDLE,  # hConsoleHandle, i.e. GetStdHandle output type
                ctypes.POINTER(wintypes.DWORD),  # result of GetConsoleHandle
            )
            kernel32.SetConsoleMode.errcheck = _err_check
            kernel32.SetConsoleMode.argtypes = (
                wintypes.HANDLE,  # hConsoleHandle, i.e. GetStdHandle output type
                wintypes.DWORD,  # result of GetConsoleHandle
            )
            # Use conout$ here to handle a redirectired stdout/get active console associated
            # with spack
            with open(r"\\.\CONOUT$", "w", encoding="utf-8") as conout:
                # Link above would use kernel32.GetStdHandle(-11) however this would not handle
                # a redirected stdout appropriately, so we always refer to the current CONSOLE out
                # which is defined as conout$ on Windows.
                # linked example is follow more or less to the letter beyond this point
                con_handle = msvcrt.get_osfhandle(conout.fileno())
                dw_orig_mode = wintypes.DWORD()
                kernel32.GetConsoleMode(con_handle, ctypes.byref(dw_orig_mode))
                dw_new_mode_request = (
                    ENABLE_VIRTUAL_TERMINAL_PROCESSING | DISABLE_NEWLINE_AUTO_RETURN
                )
                dw_new_mode = dw_new_mode_request | dw_orig_mode.value
                kernel32.SetConsoleMode(con_handle, wintypes.DWORD(dw_new_mode))
        except OSError:
            # We failed to enable color support for associated console
            # report and move on but spack will no longer attempt to
            # color
            global _force_color
            _force_color = False


def get_color_when() -> bool:
    """Return whether commands should print color or not."""
    if _force_color is not None:
        return _force_color
    return sys.stdout.isatty()


def set_color_when(when: Union[str, bool, None]) -> None:
    """Set when color should be applied.  Options are:

    * True or ``"always"``: always print color
    * False or ``"never"``: never print color
    * None or ``"auto"``: only print color if sys.stdout is a tty.
    """
    global _force_color
    _force_color = _color_when_value(when)


@contextmanager
def color_when(value: Union[str, bool, None]) -> Iterator[None]:
    """Context manager to temporarily use a particular color setting."""
    old_value = _force_color
    set_color_when(value)
    yield
    set_color_when(old_value)


_ConvertibleToStr = Union[str, int, bool, None]


def _escape(s: _ConvertibleToStr, color: bool, enclose: bool, zsh: bool) -> str:
    """Returns a TTY escape sequence for a color"""
    if not color:
        return ""
    elif zsh:
        return f"\033[0;{s}m"

    result = f"\033[{s}m"

    if enclose:
        result = rf"\[{result}\]"

    return result


def colorize(
    string: str, color: Optional[bool] = None, enclose: bool = False, zsh: bool = False
) -> str:
    """Replace all color expressions in a string with ANSI control codes.

    Args:
        string: The string to replace
        color: If False, output will be plain text without control codes, for output to
            non-console devices (default: automatically choose color or not)
        enclose: If True, enclose ansi color sequences with square brackets to prevent
            misestimation of terminal width.
        zsh: If True, use zsh ansi codes instead of bash ones (for variables like PS1)
    """
    if color is None:
        color = get_color_when()

    def match_to_ansi(match) -> str:
        """Convert a match object generated by ``COLOR_RE`` into an ansi
        color code. This can be used as a handler in ``re.sub``.
        """
        escaped_at, dot, style, color_code, text = match.groups()

        if escaped_at:
            return "@"
        elif dot:
            return _escape(0, color, enclose, zsh)
        elif not (style or color_code):
            raise ColorParseError(
                f"Incomplete color format: '{match.group(0)}' in '{match.string}'"
            )

        color_number = colors.get(color_code, "")
        semi = ";" if color_number else ""
        ansi_code = _escape(f"{styles[style]}{semi}{color_number}", color, enclose, zsh)
        if text:
            return f"{ansi_code}{text}{_escape(0, color, enclose, zsh)}"
        else:
            return ansi_code

    return COLOR_RE.sub(match_to_ansi, string).replace("}}", "}")


#: matches a standard ANSI color code
ANSI_CODE_RE = re.compile(r"\033[^m]*m")


def csub(string: str) -> str:
    """Return the string with ANSI color sequences removed."""
    return ANSI_CODE_RE.sub("", string)


class ColorMapping(NamedTuple):
    color: str  #: color string
    colors: List[str]  #: ANSI color codes in the color string, in order
    offsets: List[Tuple[int, int]]  #: map indices in plain string to offsets in color string

    def plain_to_color(self, index: int) -> int:
        """Convert plain string index to color index."""
        offset = 0
        for i, off in self.offsets:
            if i > index:
                break
            offset = off
        return index + offset


def cmapping(string: str) -> ColorMapping:
    """Return a mapping for translating indices in a plain string to indices in colored text.

    The returned dictionary maps indices in the plain string to the offset of the cooresponding
    indices in the colored string.

    """
    colors = []
    offsets = []
    color_offset = 0

    for m in ANSI_CODE_RE.finditer(string):
        start, end = m.start(), m.end()
        start_offset = color_offset
        color_offset += end - start
        offsets.append((start - start_offset, color_offset))
        colors.append(m.group())

    return ColorMapping(string, colors, offsets)


def cwrap(
    string: str, *, initial_indent: str = "", subsequent_indent: str = "", **kwargs
) -> List[str]:
    """Wrapper around ``textwrap.wrap()`` that handles ANSI color codes."""
    plain = csub(string)
    lines = textwrap.wrap(
        plain, initial_indent=initial_indent, subsequent_indent=subsequent_indent, **kwargs
    )

    # do nothing if string has no ANSI codes
    if plain == string:
        return lines

    # otherwise add colors back to lines after wrapping plain text
    cmap = cmapping(string)

    clines = []
    start = 0
    for i, line in enumerate(lines):
        # scan to find the actual start, skipping any whitespace from a prior line break
        # can assume this b/c textwrap only collapses whitespace at line breaks
        while start < len(plain) and plain[start].isspace():
            start += 1

        # map the start and end positions in the plain string to the color string
        cstart = cmap.plain_to_color(start)

        # rewind to include any color codes before cstart
        while cstart and string[cstart - 1] == "m":
            cstart = string.rfind("\033", 0, cstart - 1)

        indent = initial_indent if i == 0 else subsequent_indent
        end = start + len(line) - len(indent)
        cend = cmap.plain_to_color(end)

        # append the color line to the result
        clines.append(indent + string[cstart:cend])
        start = end

    return clines


def clen(string: str) -> int:
    """Return the length of a string, excluding ansi color sequences."""
    return len(csub(string))


def cextra(string: str) -> int:
    """Length of extra color characters in a string"""
    return len("".join(re.findall(r"\033[^m]*m", string)))


def cwrite(string: str, stream: Optional[io.IOBase] = None, color: Optional[bool] = None) -> None:
    """Replace all color expressions in string with ANSI control
    codes and write the result to the stream.  If color is
    False, this will write plain text with no color.  If True,
    then it will always write colored output.  If not supplied,
    then it will be set based on stream.isatty().
    """
    stream = sys.stdout if stream is None else stream
    if color is None:
        color = get_color_when()
    stream.write(colorize(string, color=color))


def cprint(string: str, stream: Optional[io.IOBase] = None, color: Optional[bool] = None) -> None:
    """Same as cwrite, but writes a trailing newline to the stream."""
    cwrite(string + "\n", stream, color)


def cescape(string: str) -> str:
    """Escapes special characters needed for color codes.

    Replaces the following symbols with their equivalent literal forms:

    =====  ======
    ``@``  ``@@``
    ``}``  ``}}``
    =====  ======

    Parameters:
        string (str): the string to escape

    Returns:
        (str): the string with color codes escaped
    """
    return string.replace("@", "@@").replace("}", "}}")


class ColorStream:
    def __init__(self, stream: io.IOBase, color: Optional[bool] = None) -> None:
        self._stream = stream
        self._color = color

    def write(self, string: str, *, raw: bool = False) -> None:
        raw_write = getattr(self._stream, "write")

        color = self._color
        if self._color is None:
            if raw:
                color = True
            else:
                color = get_color_when()
        raw_write(colorize(string, color=color))
