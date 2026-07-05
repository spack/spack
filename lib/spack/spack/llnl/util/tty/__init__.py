# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import io
import os
import shutil
import sys
import textwrap
import traceback
from datetime import datetime
from types import TracebackType
from typing import IO, TYPE_CHECKING, Callable, Iterator, NoReturn, Optional, Type, Union

if TYPE_CHECKING:
    from typing_extensions import Self

from spack.util.lang import memoized

from .color import cescape, clen, cprint, cwrite

# Globals
_debug = 0
_verbose = False
_stacktrace = False
_timestamp = False
_msg_enabled = True
_warn_enabled = True
_error_enabled = True
_output_filter: Callable[[str], str] = lambda s: s
indent = "  "


def debug_level() -> int:
    return _debug


def is_verbose() -> bool:
    return _verbose


def is_debug(level: int = 1) -> bool:
    return _debug >= level


def set_debug(level: int = 0) -> None:
    global _debug
    assert level >= 0, "Debug level must be a positive value"
    _debug = level


def set_verbose(flag: bool) -> None:
    global _verbose
    _verbose = flag


def set_timestamp(flag: bool) -> None:
    global _timestamp
    _timestamp = flag


def set_msg_enabled(flag: bool) -> None:
    global _msg_enabled
    _msg_enabled = flag


def set_warn_enabled(flag: bool) -> None:
    global _warn_enabled
    _warn_enabled = flag


def set_error_enabled(flag: bool) -> None:
    global _error_enabled
    _error_enabled = flag


def msg_enabled() -> bool:
    return _msg_enabled


def warn_enabled() -> bool:
    return _warn_enabled


def error_enabled() -> bool:
    return _error_enabled


@contextlib.contextmanager
def output_filter(filter_fn: Callable[[str], str]) -> Iterator[None]:
    """Context manager that applies a filter to all output."""
    global _output_filter
    saved_filter = _output_filter
    try:
        _output_filter = filter_fn
        yield
    finally:
        _output_filter = saved_filter


class SuppressOutput:
    """Class for disabling output in a scope using ``with`` keyword"""

    def __init__(
        self, msg_enabled: bool = True, warn_enabled: bool = True, error_enabled: bool = True
    ) -> None:
        self._msg_enabled_initial = _msg_enabled
        self._warn_enabled_initial = _warn_enabled
        self._error_enabled_initial = _error_enabled

        self._msg_enabled = msg_enabled
        self._warn_enabled = warn_enabled
        self._error_enabled = error_enabled

    def __enter__(self) -> None:
        set_msg_enabled(self._msg_enabled)
        set_warn_enabled(self._warn_enabled)
        set_error_enabled(self._error_enabled)

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        set_msg_enabled(self._msg_enabled_initial)
        set_warn_enabled(self._warn_enabled_initial)
        set_error_enabled(self._error_enabled_initial)


def set_stacktrace(flag: bool) -> None:
    global _stacktrace
    _stacktrace = flag


def process_stacktrace(countback: int) -> str:
    """Gives file and line frame ``countback`` frames from the bottom"""
    st = traceback.extract_stack()
    # Not all entries may be spack files, we have to remove those that aren't.
    file_list = []
    for frame in st:
        # Check that the file is a spack file
        if frame[0].find(os.path.sep + "spack") >= 0:
            file_list.append(frame[0])
    # We use commonprefix to find what the spack 'root' directory is.
    root_dir = os.path.commonprefix(file_list)
    root_len = len(root_dir)
    st_idx = len(st) - countback - 1
    st_text = f"{st[st_idx][0][root_len:]}:{st[st_idx][1]:d} "
    return st_text


def show_pid() -> bool:
    return is_debug(2)


def get_timestamp(force: bool = False) -> str:
    """Get a string timestamp"""
    if _debug or _timestamp or force:
        # Note the inclusion of the PID is useful for parallel builds.
        pid = f", {os.getpid()}" if show_pid() else ""
        return f"[{datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')}{pid}] "
    else:
        return ""


def msg(message: Union[Exception, str], *args: str, newline: bool = True) -> None:
    """Print a message to the console."""
    if not msg_enabled():
        return

    if isinstance(message, Exception):
        message = f"{message.__class__.__name__}: {message}"
    else:
        message = str(message)

    st_text = ""
    if _stacktrace:
        st_text = process_stacktrace(2)

    nl = "\n" if newline else ""
    cwrite(f"@*b{{{st_text}==>}} {get_timestamp()}{cescape(_output_filter(message))}{nl}")

    for arg in args:
        print(indent + _output_filter(str(arg)))


def info(
    message: Union[Exception, str],
    *args,
    format: str = "*b",
    stream: Optional[IO[str]] = None,
    wrap: bool = False,
    break_long_words: bool = False,
    countback: int = 3,
) -> None:
    """Print an informational message."""
    if isinstance(message, Exception):
        message = f"{message.__class__.__name__}: {str(message)}"

    stream = stream or sys.stdout
    st_text = ""
    if _stacktrace:
        st_text = process_stacktrace(countback)
    cprint(
        "@%s{%s==>} %s%s"
        % (format, st_text, get_timestamp(), cescape(_output_filter(str(message)))),
        stream=stream,
    )
    for arg in args:
        if wrap:
            lines = textwrap.wrap(
                _output_filter(str(arg)),
                initial_indent=indent,
                subsequent_indent=indent,
                break_long_words=break_long_words,
            )
            for line in lines:
                stream.write(line + "\n")
        else:
            stream.write(indent + _output_filter(str(arg)) + "\n")
    stream.flush()


def verbose(message, *args, format: str = "c", **kwargs) -> None:
    """Print a verbose message if the verbose flag is set."""
    if _verbose:
        info(message, *args, format=format, **kwargs)


def debug(
    message, *args, level: int = 1, format: str = "g", stream: Optional[IO[str]] = None, **kwargs
) -> None:
    """Print a debug message if the debug level is set."""
    if is_debug(level):
        stream_arg = stream or sys.stderr
        info(message, *args, format=format, stream=stream_arg, **kwargs)


def error(message, *args, format: str = "*r", stream: Optional[IO[str]] = None, **kwargs) -> None:
    """Print an error message."""
    if not error_enabled():
        return

    stream = stream or sys.stderr
    info(f"Error: {message}", *args, format=format, stream=stream, **kwargs)


def warn(message, *args, format: str = "*Y", stream: Optional[IO[str]] = None, **kwargs) -> None:
    """Print a warning message."""
    if not warn_enabled():
        return

    stream = stream or sys.stderr
    info(f"Warning: {message}", *args, format=format, stream=stream, **kwargs)


def die(message, *args, countback: int = 4, **kwargs) -> NoReturn:
    error(message, *args, countback=countback, **kwargs)
    sys.exit(1)


def get_yes_or_no(prompt: str, default: Optional[bool] = None) -> Optional[bool]:
    if default is None:
        prompt += " [y/n] "
    elif default is True:
        prompt += " [Y/n] "
    elif default is False:
        prompt += " [y/N] "
    else:
        raise ValueError("default for get_yes_no() must be True, False, or None.")

    result = None
    while result is None:
        msg(prompt, newline=False)
        ans = input().lower()
        if not ans:
            result = default
            if result is None:
                print("Please enter yes or no.")
        else:
            if ans == "y" or ans == "yes":
                result = True
            elif ans == "n" or ans == "no":
                result = False
    return result


class TerminalWidth(int):
    MIN_WIDTH = 10

    def __new__(cls, *args, **kwargs):
        ret = super().__new__(cls, *args, **kwargs)
        if ret <= cls.MIN_WIDTH:
            raise ValueError(
                f"selected terminal width must be at least {cls.MIN_WIDTH} columns wide "
                f"(was: {ret})"
            )
        return ret

    @classmethod
    @memoized
    def _default(cls) -> Self:
        return cls(72)

    @classmethod
    @memoized
    def _as_introspected(cls) -> Optional[Self]:
        """Query the stdlib facilities for the width of the encompassing terminal, if available."""
        cols = shutil.get_terminal_size().columns
        if cols:
            return cls(cols)
        return None

    @classmethod
    def _as_configured(cls) -> Optional[Self]:
        # May return 0 (the default), which we convert to a None.
        import spack.config

        width = spack.config.get("config:max_width")
        if width:
            return cls(width)
        return None

    @classmethod
    def configured(cls, default: Optional[Self] = None) -> Self:
        configured = cls._as_configured()
        if configured is not None:
            return configured
        introspected = cls._as_introspected()
        if introspected is not None:
            return introspected
        return default or cls._default

    @memoized
    def limit_to(self, within_range: Self) -> Self:
        if self <= within_range:
            return self
        return within_range

    def reduce_by(self, n: int) -> Self:
        """Reduce the current width by some amount."""
        if n < 0:
            raise ValueError(f"cannot reduce a terminal width by a negative (got: {n})")
        # This will raise ValueError if < the min width.
        return self.__class__(self - n)

    @classmethod
    @memoized
    def _hline_max_width(cls) -> Self:
        return cls(64)

    @classmethod
    def convert_or_default(cls, default: Self, max_width: Optional[int] = None) -> Self:
        if max_width is None:
            return default
        return cls(max_width)


def hline(
    label: Optional[str] = None, *, char: str = "-", max_width: Optional[int] = None
) -> None:
    """Draw a labeled horizontal line.

    Args:
        char: char to draw the line with
        max_width: maximum width of the line
    """
    max_width = TerminalWidth.convert_or_default(
        default=TerminalWidth._hline_max_width(), max_width=max_width
    )
    cols = TerminalWidth.configured().reduce_by(2).limit_to(max_width)

    label = str(label)
    prefix = char * 2 + " "
    suffix = " " + (cols - len(prefix) - clen(label)) * char

    out = io.StringIO()
    out.write(prefix)
    out.write(label)
    out.write(suffix)

    print(out.getvalue())
