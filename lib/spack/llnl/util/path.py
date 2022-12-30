# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Utilities for managing Linux and Windows paths."""

# TODO: look at using pathlib since we now only support Python 3

import os
import re
import sys
from urllib.parse import urlparse

is_windows = sys.platform == "win32"


def is_path_url(path):
    if "\\" in path:
        return False
    url_tuple = urlparse(path)
    return bool(url_tuple.scheme) and len(url_tuple.scheme) > 1


def win_exe_ext():
    return ".exe"


def path_to_os_path(*pths):
    """
    Takes an arbitrary number of positional parameters
    converts each arguemnt of type string to use a normalized
    filepath separator, and returns a list of all values
    """
    ret_pths = []
    for pth in pths:
        if isinstance(pth, str) and not is_path_url(pth):
            pth = convert_to_platform_path(pth)
        ret_pths.append(pth)
    return ret_pths


def sanitize_file_path(pth):
    """
    Formats strings to contain only characters that can
    be used to generate legal file paths.

    Criteria for legal files based on
    https://en.wikipedia.org/wiki/Filename#Comparison_of_filename_limitations

    Args:
        pth: string containing path to be created
            on the host filesystem

    Return:
        sanitized string that can legally be made into a path
    """
    # on unix, splitting path by seperators will remove
    # instances of illegal characters on join
    pth_cmpnts = pth.split(os.path.sep)

    if is_windows:
        drive_match = r"[a-zA-Z]:"
        is_abs = bool(re.match(drive_match, pth_cmpnts[0]))
        drive = pth_cmpnts[0] + os.path.sep if is_abs else ""
        pth_cmpnts = pth_cmpnts[1:] if drive else pth_cmpnts
        illegal_chars = r'[<>?:"|*\\]'
    else:
        drive = "/" if not pth_cmpnts[0] else ""
        illegal_chars = r"[/]"

    pth = []
    for cmp in pth_cmpnts:
        san_cmp = re.sub(illegal_chars, "", cmp)
        pth.append(san_cmp)
    return drive + os.path.join(*pth)


def system_path_filter(_func=None, arg_slice=None):
    """
    Filters function arguments to account for platform path separators.
    Optional slicing range can be specified to select specific arguments

    This decorator takes all (or a slice) of a method's positional arguments
    and normalizes usage of filepath separators on a per platform basis.

    Note: **kwargs, urls, and any type that is not a string are ignored
    so in such cases where path normalization is required, that should be
    handled by calling path_to_os_path directly as needed.

    Parameters:
        arg_slice (slice): a slice object specifying the slice of arguments
            in the decorated method over which filepath separators are
            normalized
    """
    from functools import wraps

    def holder_func(func):
        @wraps(func)
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


class Path:
    """
    Describes the filepath separator types
    in an enum style
    with a helper attribute
    exposing the path type of
    the current platform.
    """

    unix = 0
    windows = 1
    platform_path = windows if is_windows else unix


def format_os_path(path, mode=Path.unix):
    """
    Format path to use consistent, platform specific
    separators. Absolute paths are converted between
    drive letters and a prepended '/' as per platform
    requirement.

    Parameters:
        path (str): the path to be normalized, must be a string
            or expose the replace method.
        mode (Path): the path filesperator style to normalize the
            passed path to. Default is unix style, i.e. '/'
    """
    if not path:
        return path
    if mode == Path.windows:
        path = path.replace("/", "\\")
    else:
        path = path.replace("\\", "/")
    return path


def convert_to_posix_path(path):
    return format_os_path(path, mode=Path.unix)


def convert_to_windows_path(path):
    return format_os_path(path, mode=Path.windows)


def convert_to_platform_path(path):
    return format_os_path(path, mode=Path.platform_path)
