# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utilities for managing paths in Spack.

TODO: this is really part of spack.config. Consolidate it.
"""

import contextlib
import functools
import os
import re
import subprocess
import sys
from typing import List, Optional, Union
from urllib.parse import urlparse

import spack.llnl.util.tty as tty
from spack.util.lang import memoized

__all__ = []


class Path:
    """Enum to identify the path-style."""

    unix: int = 0
    windows: int = 1
    platform_path: int = windows if sys.platform == "win32" else unix


def format_os_path(path: str, mode: int = Path.unix) -> str:
    """Formats the input path to use consistent, platform specific separators.

    Absolute paths are converted between drive letters and a prepended ``/`` as per platform
    requirement.

    Parameters:
        path: the path to be normalized, must be a string or expose the replace method.
        mode: the path file separator style to normalize the passed path to.
            Default is unix style, i.e. ``/``
    """
    if not path:
        return path
    if mode == Path.windows:
        path = path.replace("/", "\\")
    else:
        path = path.replace("\\", "/")
    return path


def convert_to_posix_path(path: str) -> str:
    """Converts the input path to POSIX style."""
    return format_os_path(path, mode=Path.unix)


def convert_to_platform_path(path: str) -> str:
    """Converts the input path to the current platform's native style."""
    return format_os_path(path, mode=Path.platform_path)


def path_to_os_path(*parameters: str) -> List[str]:
    """Takes an arbitrary number of positional parameters, converts each argument of type
    string to use a normalized filepath separator, and returns a list of all values.
    """

    def _is_url(path_or_url: str) -> bool:
        if "\\" in path_or_url:
            return False
        url_tuple = urlparse(path_or_url)
        return bool(url_tuple.scheme) and len(url_tuple.scheme) > 1

    result = []
    for item in parameters:
        if isinstance(item, str) and not _is_url(item):
            item = convert_to_platform_path(item)
        result.append(item)
    return result


def _system_path_filter(_func=None, arg_slice: Optional[slice] = None):
    """Filters function arguments to account for platform path separators.
    Optional slicing range can be specified to select specific arguments

    This decorator takes all (or a slice) of a method's positional arguments
    and normalizes usage of filepath separators on a per platform basis.

    Note: `**kwargs`, urls, and any type that is not a string are ignored
    so in such cases where path normalization is required, that should be
    handled by calling path_to_os_path directly as needed.

    Parameters:
        arg_slice: a slice object specifying the slice of arguments
            in the decorated method over which filepath separators are
            normalized
    """

    def holder_func(func):
        @functools.wraps(func)
        def path_filter_caller(*args, **kwargs):
            args = list(args)
            if arg_slice:
                args[arg_slice] = path_to_os_path(*args[arg_slice])
            else:
                args = path_to_os_path(*args)
            return func(*args, **kwargs)

        return path_filter_caller

    if _func:
        return holder_func(_func)
    return holder_func


def _noop_decorator(_func=None, arg_slice: Optional[slice] = None):
    return _func if _func else lambda x: x


if sys.platform == "win32":
    system_path_filter = _system_path_filter
else:
    system_path_filter = _noop_decorator


def sanitize_win_longpath(path: str) -> str:
    """Strip Windows extended path prefix from strings
    Returns sanitized string.
    no-op if extended path prefix is not present"""
    return path.lstrip("\\\\?\\")


# This is intended to be longer than the part of the install path
# spack generates from the root path we give it.  Included in the
# estimate:
#
#   os-arch      ->   30
#   compiler     ->   30
#   package name ->   50   (longest is currently 47 characters)
#   version      ->   20
#   hash         ->   32
#   buffer       ->  138
#  ---------------------
#   total        ->  300
SPACK_MAX_INSTALL_PATH_LENGTH = 300

#: Padded paths comprise directories with this name (or some prefix of it). :
#: It starts with two underscores to make it unlikely that prefix matches would
#: include some other component of the installation path.
SPACK_PATH_PADDING_CHARS = "__spack_path_placeholder__"

#: Bytes equivalent of SPACK_PATH_PADDING_CHARS.
SPACK_PATH_PADDING_BYTES = SPACK_PATH_PADDING_CHARS.encode("ascii")

#: Special padding char if the padded string would otherwise end with a path
#: separator (since the path separator would otherwise get collapsed out,
#: causing inconsistent padding).
SPACK_PATH_PADDING_EXTRA_CHAR = "_"


def win_exe_ext():
    return r"(?:\.bat|\.exe)"


def sanitize_filename(filename: str) -> str:
    """
    Replaces unsupported characters (for the host) in a filename with underscores.

    Criteria for legal files based on
    https://en.wikipedia.org/wiki/Filename#Comparison_of_filename_limitations

    Args:
        filename: string containing filename to be created on the host filesystem

    Return:
        filename that can be created on the host filesystem
    """
    if sys.platform != "win32":
        # Only disallow null bytes and directory separators.
        return re.sub("[\0/]", "_", filename)

    # On Windows, things are more involved.
    # NOTE: this is incomplete, missing reserved names
    return re.sub(r'[\x00-\x1F\x7F"*/:<>?\\|]', "_", filename)


@memoized
def get_system_path_max():
    # Choose a conservative default
    sys_max_path_length = 256
    if sys.platform == "win32":
        sys_max_path_length = 260
    else:
        try:
            path_max_proc = subprocess.Popen(
                ["getconf", "PATH_MAX", "/"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            proc_output = str(path_max_proc.communicate()[0].decode())
            sys_max_path_length = int(proc_output)
        except (ValueError, subprocess.CalledProcessError, OSError):
            tty.msg(
                "Unable to find system max path length, using: {0}".format(sys_max_path_length)
            )

    return sys_max_path_length


def _get_padding_string(length):
    spack_path_padding_size = len(SPACK_PATH_PADDING_CHARS)
    num_reps = int(length / (spack_path_padding_size + 1))
    extra_chars = length % (spack_path_padding_size + 1)
    reps_list = [SPACK_PATH_PADDING_CHARS for i in range(num_reps)]
    reps_list.append(SPACK_PATH_PADDING_CHARS[:extra_chars])
    padding = os.path.sep.join(reps_list)
    if padding.endswith(os.path.sep):
        padding = padding[: len(padding) - 1] + SPACK_PATH_PADDING_EXTRA_CHAR
    return padding


def add_padding(path, length):
    """Add padding subdirectories to path until total is length characters

    Returns the padded path. If path is length - 1 or more characters long,
    returns path. If path is length - 1 characters, warns that it is not
    padding to length

    Assumes path does not have a trailing path separator"""
    padding_length = length - len(path)
    if padding_length == 1:
        # The only 1 character addition we can make to a path is `/`
        # Spack internally runs normpath, so `foo/` will be reduced to `foo`
        # Even if we removed this behavior from Spack, the user could normalize
        # the path, removing the additional `/`.
        # Because we can't expect one character of padding to show up in the
        # resulting binaries, we warn the user and do not pad by a single char
        tty.warn("Cannot pad path by exactly one character.")
    if padding_length <= 0:
        return path

    # we subtract 1 from the padding_length to account for the path separator
    # coming from os.path.join below
    padding = _get_padding_string(padding_length - 1)

    return os.path.join(path, padding)


def longest_prefix_re(string, capture=True):
    """Return a regular expression that matches a the longest possible prefix of string.

    i.e., if the input string is ``the_quick_brown_fox``, then::

        m = re.compile(longest_prefix('the_quick_brown_fox'))
        m.match('the_').group(1)                 == 'the_'
        m.match('the_quick').group(1)            == 'the_quick'
        m.match('the_quick_brown_fox').group(1)  == 'the_quick_brown_fox'
        m.match('the_xquick_brown_fox').group(1) == 'the_'
        m.match('the_quickx_brown_fox').group(1) == 'the_quick'

    """
    if len(string) < 2:
        return string

    return "(%s%s%s?)" % (
        "" if capture else "?:",
        string[0],
        longest_prefix_re(string[1:], capture=False),
    )


def _build_padding_re(as_bytes: bool = False):
    """Build and return a compiled regex for filtering path padding placeholders."""
    pad = re.escape(SPACK_PATH_PADDING_CHARS)
    extra = SPACK_PATH_PADDING_EXTRA_CHAR
    longest_prefix = longest_prefix_re(SPACK_PATH_PADDING_CHARS, capture=False)

    regex = (
        r"((?:/[^/\s]*)*?)"  # zero or more leading non-whitespace path components
        r"(?:/{pad})+"  # the padding string repeated one or more times
        # trailing prefix of padding as path component
        r"(?:/{longest_prefix}|/{longest_prefix}{extra})?(?=/)"
    )
    regex = regex.replace("/", re.escape(os.sep))
    regex = regex.format(pad=pad, extra=extra, longest_prefix=longest_prefix)

    if as_bytes:
        return re.compile(regex.encode("ascii"))
    else:
        return re.compile(regex)


class _PaddingFilter:
    """Callable that filters path-padding placeholders from a string or bytes buffer.

    This turns paths like this:

        /foo/bar/__spack_path_placeholder__/__spack_path_placeholder__/...

    Into paths like this:

        /foo/bar/[padded-to-512-chars]/...

    Where ``padded-to-512-chars`` indicates that the prefix was padded with
    placeholders until it hit 512 characters. The actual value of this number
    depends on what the ``install_tree``'s ``padded_length`` is configured to.

    For a path to match and be filtered, the placeholder must appear in its
    entirety at least one time. e.g., "/spack/" would not be filtered, but
    "/__spack_path_placeholder__/spack/" would be.

    Note that only the first padded path in the string is filtered.
    """

    __slots__ = ("_re", "_needle", "_fmt")

    def __init__(self, as_bytes: bool = False) -> None:
        self._re = _build_padding_re(as_bytes=as_bytes)
        if as_bytes:
            self._needle: Union[str, bytes] = SPACK_PATH_PADDING_BYTES
            self._fmt: Union[str, bytes] = b"%b" + os.sep.encode("ascii") + b"[padded-to-%d-chars]"
        else:
            self._needle = SPACK_PATH_PADDING_CHARS
            self._fmt = "%s" + os.sep + "[padded-to-%d-chars]"

    def _replace(self, match):
        return self._fmt % (match.group(1), len(match.group(0)))

    def __call__(self, data):
        if self._needle not in data:
            return data
        return self._re.sub(self._replace, data)


#: Callable that filters path-padding placeholders from strings
padding_filter = _PaddingFilter(as_bytes=False)

#: Callable that filters path-padding placeholders from bytes buffers
padding_filter_bytes = _PaddingFilter(as_bytes=True)


@contextlib.contextmanager
def filter_padding():
    """Context manager to safely disable path padding in all Spack output.

    This is needed because Spack's debug output gets extremely long when we use a
    long padded installation path.
    """
    # circular import
    import spack.config

    padding = spack.config.get("config:install_tree:padded_length", None)
    if padding:
        # filter out all padding from the install command output
        with tty.output_filter(padding_filter):
            yield
    else:
        yield  # no-op: don't filter unless padding is actually enabled


def debug_padded_filter(string, level=1):
    """
    Return string, path padding filtered if debug level and not windows

    Args:
        string (str): string containing path
        level (int): maximum debug level value for filtering (e.g., 1
            means filter path padding if the current debug level is 0 or 1
            but return the original string if it is 2 or more)

    Returns (str): filtered string if current debug level does not exceed
        level and not windows; otherwise, unfiltered string
    """
    if sys.platform == "win32":
        return string

    return padding_filter(string) if tty.debug_level() <= level else string
