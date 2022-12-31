# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import shlex
import subprocess
import sys
from typing import List, Optional, Union

import llnl.util.tty as tty
from llnl.util.path import Path, format_os_path, path_to_os_path, system_path_filter

__all__ = ["Executable", "which", "ProcessError"]


class Executable(object):
    """Class representing a program that can be run on the command line."""

    def __init__(self, name):
        # necesary here for the shlex call to succeed
        name = format_os_path(name, mode=Path.unix)
        self.exe = shlex.split(str(name))
        # filter back to platform dependent path
        self.exe = path_to_os_path(*self.exe)
        self.default_env = {}
        self._default_envmod = None
        self.returncode = None

        if not self.exe:
            raise ProcessError(f"Cannot construct executable for '{name}'")

    @property
    def default_envmod(self):
        from llnl.util.envmod import EnvironmentModifications

        if self._default_envmod is None:
            self._default_envmod = EnvironmentModifications()

        return self._default_envmod

    @system_path_filter
    def add_default_arg(self, arg):
        """Add a default argument to the command."""
        self.exe.append(arg)

    @system_path_filter
    def add_default_env(self, key, value):
        """Set an environment variable when the command is run.

        Parameters:
            key: The environment variable to set
            value: The value to set it to
        """
        self.default_env[key] = value

    def add_default_envmod(self, envmod):
        """Set an EnvironmentModifications to use when the command is run."""
        self.default_envmod.extend(envmod)

    @property
    def command(self):
        """The command-line string.

        Returns:
            str: The executable and default arguments
        """
        return " ".join(self.exe)

    @property
    def name(self):
        """The executable name.

        Returns:
            str: The basename of the executable
        """
        return os.path.basename(self.path)

    @property
    def path(self):
        """The path to the executable.

        Returns:
            str: The path to the executable
        """
        return self.exe[0]

    def __call__(self, *args, **kwargs):
        """Run this executable in a subprocess.

        Parameters:
            *args (str): Command-line arguments to the executable to run

        Keyword Arguments:
            _dump_env (dict): Dict to be set to the environment actually
                used (envisaged for testing purposes only)
            env (dict or EnvironmentModifications): The environment with which
                to run the executable
            extra_env (dict or EnvironmentModifications): Extra items to add to
                the environment (neither requires nor precludes env)
            fail_on_error (bool): Raise an exception if the subprocess returns
                an error. Default is True. The return code is available as
                ``exe.returncode``
            ignore_errors (int or list): A list of error codes to ignore.
                If these codes are returned, this process will not raise
                an exception even if ``fail_on_error`` is set to ``True``
            ignore_quotes (bool): If False, warn users that quotes are not needed
                as Spack does not use a shell. Defaults to False.
            input: Where to read stdin from
            output: Where to send stdout
            error: Where to send stderr

        Accepted values for input, output, and error:

        * python streams, e.g. open Python file objects, or ``os.devnull``
        * filenames, which will be automatically opened for writing
        * ``str``, as in the Python string type. If you set these to ``str``,
          output and error will be written to pipes and returned as a string.
          If both ``output`` and ``error`` are set to ``str``, then one string
          is returned containing output concatenated with error. Not valid
          for ``input``
        * ``str.split``, as in the ``split`` method of the Python string type.
          Behaves the same as ``str``, except that value is also written to
          ``stdout`` or ``stderr``.

        By default, the subprocess inherits the parent's file descriptors.

        """
        from llnl.util.envmod import EnvironmentModifications

        # Environment
        env_arg = kwargs.get("env", None)

        # Setup default environment
        env = os.environ.copy() if env_arg is None else {}
        self.default_envmod.apply_modifications(env)
        env.update(self.default_env)

        # Apply env argument
        if isinstance(env_arg, EnvironmentModifications):
            env_arg.apply_modifications(env)
        elif env_arg:
            env.update(env_arg)

        # Apply extra env
        extra_env = kwargs.get("extra_env", {})
        if isinstance(extra_env, EnvironmentModifications):
            extra_env.apply_modifications(env)
        else:
            env.update(extra_env)

        if "_dump_env" in kwargs:
            kwargs["_dump_env"].clear()
            kwargs["_dump_env"].update(env)

        fail_on_error = kwargs.pop("fail_on_error", True)
        ignore_errors = kwargs.pop("ignore_errors", ())
        ignore_quotes = kwargs.pop("ignore_quotes", False)

        # If they just want to ignore one error code, make it a tuple.
        if isinstance(ignore_errors, int):
            ignore_errors = (ignore_errors,)

        input = kwargs.pop("input", None)
        output = kwargs.pop("output", None)
        error = kwargs.pop("error", None)

        if input is str:
            raise ValueError("Cannot use `str` as input stream.")

        def streamify(arg, mode):
            if isinstance(arg, str):
                return open(arg, mode), True
            elif arg in (str, str.split):
                return subprocess.PIPE, False
            else:
                return arg, False

        ostream, close_ostream = streamify(output, "w")
        estream, close_estream = streamify(error, "w")
        istream, close_istream = streamify(input, "r")

        if not ignore_quotes:
            quoted_args = [arg for arg in args if re.search(r'^".*"$|^\'.*\'$', arg)]
            if quoted_args:
                tty.warn(
                    "Quotes in command arguments can confuse scripts like" " configure.",
                    "The following arguments may cause problems when executed:",
                    str("\n".join(["    " + arg for arg in quoted_args])),
                    "Quotes aren't needed because spack doesn't use a shell. "
                    "Consider removing them.",
                    "If multiple levels of quotation are required, use " "`ignore_quotes=True`.",
                )

        cmd = self.exe + list(args)

        escaped_cmd = ["'%s'" % arg.replace("'", "'\"'\"'") for arg in cmd]
        cmd_line_string = " ".join(escaped_cmd)
        tty.debug(cmd_line_string)

        try:
            proc = subprocess.Popen(
                cmd,
                stdin=istream,
                stderr=estream,
                stdout=ostream,
                env=env,
                close_fds=False,
            )
            out, err = proc.communicate()

            result = None
            if output in (str, str.split) or error in (str, str.split):
                result = ""
                if output in (str, str.split):
                    if sys.platform == "win32":
                        outstr = str(out.decode("ISO-8859-1"))
                    else:
                        outstr = str(out.decode("utf-8"))
                    result += outstr
                    if output is str.split:
                        sys.stdout.write(outstr)
                if error in (str, str.split):
                    if sys.platform == "win32":
                        errstr = str(err.decode("ISO-8859-1"))
                    else:
                        errstr = str(err.decode("utf-8"))
                    result += errstr
                    if error is str.split:
                        sys.stderr.write(errstr)

            rc = self.returncode = proc.returncode
            if fail_on_error and rc != 0 and (rc not in ignore_errors):
                msg = f"Command {cmd_line_string} exited with status {proc.returncode}."
                if result:
                    # If the output is not captured in the result, it will have
                    # been stored either in the specified files (e.g. if
                    # 'output' specifies a file) or written to the parent's
                    # stdout/stderr (e.g. if 'output' is not specified)
                    msg += "\n" + result

                raise ProcessError(msg)

            return result

        except OSError as e:
            raise ProcessError(f"{self.exe[0]}: {e.strerror}\n    Command: '{cmd_line_string}'")

        except subprocess.CalledProcessError as e:
            if fail_on_error:
                raise ProcessError(
                    f"{str(e)}\n"
                    f"    Exit status {proc.returncode} when invoking command: '{cmd_line_string}'"
                )

        finally:
            if close_ostream:
                ostream.close()
            if close_estream:
                estream.close()
            if close_istream:
                istream.close()

    def __eq__(self, other):
        return hasattr(other, "exe") and self.exe == other.exe

    def __neq__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((type(self),) + tuple(self.exe))

    def __repr__(self):
        return "<exe: %s>" % self.exe

    def __str__(self):
        return " ".join(self.exe)


@system_path_filter
def which_string(*args: str, path: Optional[Union[List[str], str]] = None, required: bool = False):
    """Finds an executable in the path like command-line which.

    If given multiple executables, returns the first one that is found.
    If no executables are found, returns None.

    Parameters:
        *args: One or more executables to search for

    Keyword Arguments:
        path: colon-separated (semicolon-separated on windows) string or list of
            paths to search. Defaults to ``os.environ["PATH"]``
        required: If set to ``True``, raise an error if executable not found

    Returns:
        Absolute path of the first executable found.
    """
    if path is None:
        path = os.environ.get("PATH") or ""

    if isinstance(path, str):
        path = path.split(os.pathsep)

    for name in args:
        win_candidates: List[str] = []
        if sys.platform == "win32" and (not name.endswith(".exe") and not name.endswith(".bat")):
            win_candidates = [name + ext for ext in [".exe", ".bat"]]
        candidate_names = [name] if not win_candidates else win_candidates

        if sys.platform == "win32":
            new_path = path[:]
            for p in path:
                if os.path.basename(p) == "bin":
                    new_path.append(os.path.dirname(p))
            path = new_path

        for candidate_name in candidate_names:
            if os.path.sep in candidate_name:
                exe = os.path.abspath(candidate_name)
                if os.path.isfile(exe) and os.access(exe, os.X_OK):
                    return exe
            else:
                for directory in path:
                    directory = path_to_os_path(directory).pop()
                    exe = os.path.join(directory, candidate_name)
                    if os.path.isfile(exe) and os.access(exe, os.X_OK):
                        return exe

    if required:
        raise CommandNotFoundError(args[0])

    return None


def which(*args: str, path: Optional[Union[List[str], str]] = None, required: bool = False):
    """Finds an executable in the path like command-line which.

    If given multiple executables, returns the first one that is found.
    If no executables are found, returns None.

    Parameters:
        *args: One or more executables to search for

    Keyword Arguments:
        path (list or str): The path to search. Defaults to ``PATH``
        required (bool): If set to True, raise an error if executable not found

    Returns:
        Executable: The first executable that is found in the path
    """
    exe = which_string(*args, path=path, required=required)
    return Executable(shlex.quote(exe)) if exe else None


class ProcessError(Exception):
    """ProcessErrors are raised when Executables exit with an error code."""


class CommandNotFoundError(Exception):
    """Raised when ``which()`` can't find a required executable."""

    def __init__(self, command: str):
        super().__init__(f"Couldn't find command '{command}'. Make sure it is in your path.")
        self.command = command
