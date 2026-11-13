# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Module for finding the user's preferred text editor.

Defines one function, editor(), which invokes the editor defined by the
user's VISUAL environment variable if set. We fall back to the editor
defined by the EDITOR environment variable if VISUAL is not set or the
specified editor fails (e.g. no DISPLAY for a graphical editor). If
neither variable is set, we fall back to one of several common editors,
raising an OSError if we are unable to find one.
"""

import os
import re
import shlex
import subprocess
import sys
from typing import Callable, Iterator, List, Optional, Tuple

import spack.util.executable
from spack.util import tty

#: editors to try if VISUAL and EDITOR are not set
_default_editors = ["vim", "vi", "emacs", "nano", "notepad"]


def _split_windows_args(args: str) -> List[str]:
    """Split a Windows command line string into arguments, following the MSVC runtime rules.

    Whitespace separates arguments, double quotes group them, and backslashes are literal
    unless they precede a double quote (``2n`` backslashes + ``"`` yield ``n`` backslashes and
    toggle quoting, ``2n+1`` backslashes + ``"`` yield ``n`` backslashes and a literal ``"``).
    """
    result: List[str] = []
    current: Optional[str] = None
    in_quotes = False
    for match in re.finditer(r'(\\*)"|(\\+)|(\s+)|([^\\"\s]+)', args):
        slashes_before_quote, slashes, space, text = match.groups()
        if space is not None and not in_quotes:
            if current is not None:
                result.append(current)
                current = None
            continue
        current = current or ""
        if slashes_before_quote is not None:
            current += "\\" * (len(slashes_before_quote) // 2)
            if len(slashes_before_quote) % 2:
                current += '"'
            else:
                in_quotes = not in_quotes
        else:
            current += slashes or space or text
    if current is not None:
        result.append(current)
    return result


def _windows_exe_candidates(value: str) -> Iterator[Tuple[str, List[str]]]:
    """Yield possible ``(program, args)`` splits of a Windows command line, in the order
    ``CreateProcess`` would try them."""
    if value.startswith('"'):
        program, _, rest = value[1:].partition('"')
        yield program, _split_windows_args(rest)
        return

    # An unquoted program path may contain spaces (e.g. C:\Program Files\...), so like
    # CreateProcess, try each whitespace-delimited prefix, shortest first.
    for match in re.finditer(r"\s+|$", value):
        yield value[: match.start()], _split_windows_args(value[match.end() :])


def _find_exe_from_env_var(var: str) -> Tuple[Optional[str], List[str]]:
    """Find an executable from an environment variable.

    Args:
        var: environment variable name

    Returns:
        executable path (or None if not found) and the full argument list parsed from the env
        var, starting with the executable path itself (i.e. ``argv`` for ``os.execv``)
    """
    value = os.environ.get(var, "").strip()
    if not value:
        return None, []

    # split env var into executable and args if needed
    if sys.platform == "win32":
        # backslashes are path separators on Windows, not escapes, so shlex can't be used
        candidates: Iterator[Tuple[str, List[str]]] = _windows_exe_candidates(value)
    else:
        args = shlex.split(value)
        candidates = iter([(args[0], args[1:])] if args else [])

    for program, args in candidates:
        exe = spack.util.executable.which_string(program)
        if exe:
            return exe, [exe] + args

    return None, []


def _execv(exe: str, args: List[str]) -> int:
    """``os.execv()``, with arguments quoted on Windows.

    The Windows CRT builds the child's command line by joining ``args`` with spaces and no
    quoting, so any argument containing whitespace (like an executable under
    ``C:\\Program Files``) is split apart by the child. ``argv[0]`` must still be passed, since
    the child parses its own program name from the start of the command line.
    """
    if sys.platform == "win32":
        args = [subprocess.list2cmdline([arg]) for arg in args]
    os.execv(exe, args)


def executable(exe: str, args: List[str]) -> int:
    """Wrapper that makes ``spack.util.executable.Executable`` look like ``os.execv()``.

    Use this with ``editor()`` if you want it to return instead of running ``execv``.
    """
    cmd = spack.util.executable.Executable(exe)
    cmd(*args[1:], fail_on_error=False)
    return cmd.returncode


def editor(*args: str, exec_fn: Callable[[str, List[str]], int] = _execv) -> bool:
    """Invoke the user's editor.

    This will try to execute the following, in order:

    1. ``$VISUAL <args>``: the "visual" editor (per POSIX)
    2. ``$EDITOR <args>``: the regular editor (per POSIX)
    3. some default editor (see ``_default_editors``) with <args>

    If an environment variable isn't defined, it is skipped.  If it
    points to something that can't be executed, we'll print a
    warning. And if we can't find anything that can be executed after
    searching the full list above, we'll raise an error.

    Arguments:
        args: args to pass to editor

        exec_fn: invoke this function to run; use ``spack.util.editor.executable`` if you
            want something that returns, instead of the default ``os.execv()``.
    """

    def try_exec(exe, args, var=None):
        """Try to execute an editor with execv, and warn if it fails.

        Returns: (bool) False if the editor failed, ideally does not
            return if ``execv`` succeeds, and ``True`` if the
            ``exec`` does return successfully.
        """
        # gvim runs in the background by default so we force it to run
        # in the foreground to ensure it gets attention.
        if "gvim" in exe and "-f" not in args:
            exe, *rest = args
            args = [exe, "-f"] + rest

        try:
            return exec_fn(exe, args) == 0

        except (OSError, spack.util.executable.ProcessError) as e:
            # Show variable we were trying to use, if it's from one
            if var:
                exe = "$%s (%s)" % (var, exe)
            tty.warn("Could not execute %s due to error:" % exe, str(e))
            return False

    def try_env_var(var):
        """Find an editor from an environment variable and try to exec it.

        This will warn if the variable points to something is not
        executable, or if there is an error when trying to exec it.
        """
        if var not in os.environ:
            return False

        exe, editor_args = _find_exe_from_env_var(var)
        if not exe:
            tty.warn("$%s is not an executable:" % var, os.environ[var])
            return False

        full_args = editor_args + list(args)
        return try_exec(exe, full_args, var)

    # try standard environment variables
    if try_env_var("SPACK_EDITOR"):
        return True
    if try_env_var("VISUAL"):
        return True
    if try_env_var("EDITOR"):
        return True

    # nothing worked -- try the first default we can find don't bother
    # trying them all -- if we get here and one fails, something is
    # probably much more deeply wrong with the environment.
    exe = spack.util.executable.which_string(*_default_editors)
    if exe and try_exec(exe, [exe] + list(args)):
        return True

    # Fail if nothing could be found
    raise OSError(
        "No text editor found! Please set the VISUAL and/or EDITOR "
        "environment variable(s) to your preferred text editor."
    )
