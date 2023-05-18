# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utilities for managing paths in Spack.

TODO: this is really part of spack.config. Consolidate it.
"""
import contextlib
import getpass
import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from urllib.parse import urlparse

import llnl.util.tty as tty
from llnl.util.lang import memoized

import spack.util.spack_yaml as syaml

__all__ = ["substitute_config_variables", "substitute_path_variables", "canonicalize_path"]


def architecture():
    # break circular import
    import spack.platforms
    import spack.spec

    host_platform = spack.platforms.host()
    host_os = host_platform.operating_system("default_os")
    host_target = host_platform.target("default_target")

    return spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))


def get_user():
    # User pwd where available because it accounts for effective uids when using ksu and similar
    try:
        # user pwd for unix systems
        import pwd

        return pwd.getpwuid(os.geteuid()).pw_name
    except ImportError:
        # fallback on getpass
        return getpass.getuser()


# return value for replacements with no match
NOMATCH = object()


# Substitutions to perform
def replacements():
    # break circular imports
    import spack.environment as ev
    import spack.paths

    arch = architecture()

    return {
        "spack": lambda: spack.paths.prefix,
        "user": lambda: get_user(),
        "tempdir": lambda: tempfile.gettempdir(),
        "user_cache_path": lambda: spack.paths.user_cache_path,
        "architecture": lambda: arch,
        "arch": lambda: arch,
        "platform": lambda: arch.platform,
        "operating_system": lambda: arch.os,
        "os": lambda: arch.os,
        "target": lambda: arch.target,
        "target_family": lambda: arch.target.microarchitecture.family,
        "date": lambda: date.today().strftime("%Y-%m-%d"),
        "env": lambda: ev.active_environment().path if ev.active_environment() else NOMATCH,
    }


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
#: include some other component of the intallation path.
SPACK_PATH_PADDING_CHARS = "__spack_path_placeholder__"


def is_path_url(path):
    if "\\" in path:
        return False
    url_tuple = urlparse(path)
    return bool(url_tuple.scheme) and len(url_tuple.scheme) > 1


def win_exe_ext():
    return ".exe"


def find_sourceforge_suffix(path):
    """find and match sourceforge filepath components
    Return match object"""
    match = re.search(r"(.*(?:sourceforge\.net|sf\.net)/.*)(/download)$", path)
    if match:
        return match.groups()
    return path, ""


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

    if sys.platform == "win32":
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
    platform_path = windows if sys.platform == "win32" else unix


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


def substitute_config_variables(path):
    """Substitute placeholders into paths.

    Spack allows paths in configs to have some placeholders, as follows:

    - $env               The active Spack environment.
    - $spack             The Spack instance's prefix
    - $tempdir           Default temporary directory returned by tempfile.gettempdir()
    - $user              The current user's username
    - $user_cache_path   The user cache directory (~/.spack, unless overridden)
    - $architecture      The spack architecture triple for the current system
    - $arch              The spack architecture triple for the current system
    - $platform          The spack platform for the current system
    - $os                The OS of the current system
    - $operating_system  The OS of the current system
    - $target            The ISA target detected for the system
    - $target_family     The family of the target detected for the system
    - $date              The current date (YYYY-MM-DD)

    These are substituted case-insensitively into the path, and users can
    use either ``$var`` or ``${var}`` syntax for the variables. $env is only
    replaced if there is an active environment, and should only be used in
    environment yaml files.
    """
    _replacements = replacements()

    # Look up replacements
    def repl(match):
        m = match.group(0)
        key = m.strip("${}").lower()
        repl = _replacements.get(key, lambda: m)()
        return m if repl is NOMATCH else str(repl)

    # Replace $var or ${var}.
    return re.sub(r"(\$\w+\b|\$\{\w+\})", repl, path)


def substitute_path_variables(path):
    """Substitute config vars, expand environment vars, expand user home."""
    path = substitute_config_variables(path)
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    return path


def _get_padding_string(length):
    spack_path_padding_size = len(SPACK_PATH_PADDING_CHARS)
    num_reps = int(length / (spack_path_padding_size + 1))
    extra_chars = length % (spack_path_padding_size + 1)
    reps_list = [SPACK_PATH_PADDING_CHARS for i in range(num_reps)]
    reps_list.append(SPACK_PATH_PADDING_CHARS[:extra_chars])
    return os.path.sep.join(reps_list)


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


def canonicalize_path(path, default_wd=None):
    """Same as substitute_path_variables, but also take absolute path.

    If the string is a yaml object with file annotations, make absolute paths
    relative to that file's directory.
    Otherwise, use ``default_wd`` if specified, otherwise ``os.getcwd()``

    Arguments:
        path (str): path being converted as needed

    Returns:
        (str): An absolute path with path variable substitution
    """
    # Get file in which path was written in case we need to make it absolute
    # relative to that path.
    filename = None
    if isinstance(path, syaml.syaml_str):
        filename = os.path.dirname(path._start_mark.name)
        assert path._start_mark.name == path._end_mark.name

    path = substitute_path_variables(path)
    if not os.path.isabs(path):
        if filename:
            path = os.path.join(filename, path)
        else:
            base = default_wd or os.getcwd()
            path = os.path.join(base, path)
            tty.debug("Using working directory %s as base for abspath" % base)

    return os.path.normpath(path)


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


#: regex cache for padding_filter function
_filter_re = None


def padding_filter(string):
    """Filter used to reduce output from path padding in log output.

    This turns paths like this:

        /foo/bar/__spack_path_placeholder__/__spack_path_placeholder__/...

    Into paths like this:

        /foo/bar/[padded-to-512-chars]/...

    Where ``padded-to-512-chars`` indicates that the prefix was padded with
    placeholders until it hit 512 characters. The actual value of this number
    depends on what the `install_tree``'s ``padded_length`` is configured to.

    For a path to match and be filtered, the placeholder must appear in its
    entirety at least one time. e.g., "/spack/" would not be filtered, but
    "/__spack_path_placeholder__/spack/" would be.

    Note that only the first padded path in the string is filtered.
    """
    global _filter_re

    pad = SPACK_PATH_PADDING_CHARS
    if not _filter_re:
        longest_prefix = longest_prefix_re(pad)
        regex = (
            r"((?:/[^/\s]*)*?)"  # zero or more leading non-whitespace path components
            r"(/{pad})+"  # the padding string repeated one or more times
            r"(/{longest_prefix})?(?=/)"  # trailing prefix of padding as path component
        )
        regex = regex.replace("/", os.sep)
        regex = regex.format(pad=pad, longest_prefix=longest_prefix)
        _filter_re = re.compile(regex)

    def replacer(match):
        return "%s%s[padded-to-%d-chars]" % (match.group(1), os.sep, len(match.group(0)))

    return _filter_re.sub(replacer, string)


@contextlib.contextmanager
def filter_padding():
    """Context manager to safely disable path padding in all Spack output.

    This is needed because Spack's debug output gets extremely long when we use a
    long padded installation path.
    """
    import spack.config

    padding = spack.config.get("config:install_tree:padded_length", None)
    if padding:
        # filter out all padding from the intsall command output
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
