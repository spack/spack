# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path, PurePath
from typing import BinaryIO, Callable, Dict, List, Optional, Sequence, Tuple, Type, Union, overload

from spack.vendor.typing_extensions import Literal

import spack.error
import spack.llnl.util.tty as tty
from spack.util.environment import EnvironmentModifications

__all__ = ["Executable", "which", "which_string", "ProcessError"]

OutType = Union[Optional[BinaryIO], str, Type[str], Callable]


def _process_cmd_output(
    out: bytes,
    err: bytes,
    output: OutType,
    error: OutType,
    encoding: str = "ISO-8859-1" if sys.platform == "win32" else "utf-8",
) -> Optional[str]:
    if output is str or output is str.split or error is str or error is str.split:
        result = ""
        if output is str or output is str.split:
            outstr = out.decode(encoding)
            result += outstr
            if output is str.split:
                sys.stdout.write(outstr)
        if error is str or error is str.split:
            errstr = err.decode(encoding)
            result += errstr
            if error is str.split:
                sys.stderr.write(errstr)
        return result
    else:
        return None


def _streamify_output(arg: OutType, name: str) -> Tuple[Union[int, BinaryIO, None], bool]:
    if isinstance(arg, str):
        return open(arg, "wb"), True
    elif arg is str or arg is str.split:
        return subprocess.PIPE, False
    elif callable(arg):
        raise ValueError(f"`{name}` must be a stream, a filename, or `str`/`str.split`")
    else:
        return arg, False


class Executable:
    """
    Represent an executable file that can be run as a subprocess.

    This class provides a simple interface for running executables with custom arguments and
    environment variables. It supports setting default arguments and environment modifications,
    copying instances, and running commands with various options for input/output/error handling.

    Example usage:

    .. code-block:: python

        ls = Executable("ls")
        ls.add_default_arg("-l")
        ls.add_default_env("LC_ALL", "C")
        output = ls("-a", output=str)  # Run 'ls -l -a' and capture output as string
    """

    def __init__(self, name: Union[str, Path]) -> None:
        file_path = str(Path(name))
        if sys.platform != "win32" and isinstance(name, str) and name.startswith("."):
            # pathlib strips the ./ from relative paths so it must be added back
            file_path = os.path.join(".", file_path)

        self.exe = [file_path]
        self._default_env: Dict[str, str] = {}
        self._default_envmod = EnvironmentModifications()
        #: Return code of the last executed command.
        self.returncode: int = 1  # 1 until proven successful
        #: Whether to warn users that quotes are not needed, as Spack does not use a shell.
        self.ignore_quotes: bool = False

    def add_default_arg(self, *args: str) -> None:
        """Add default argument(s) to the command."""
        self.exe.extend(args)

    def with_default_args(self, *args: str) -> "Executable":
        """Same as add_default_arg, but returns a copy of the executable."""
        new = self.copy()
        new.add_default_arg(*args)
        return new

    def copy(self) -> "Executable":
        """Return a copy of this Executable."""
        new = Executable(self.exe[0])
        new.exe[:] = self.exe
        new._default_env.update(self._default_env)
        new._default_envmod.extend(self._default_envmod)
        return new

    def add_default_env(self, key: str, value: str) -> None:
        """Set an environment variable when the command is run.

        Parameters:
            key: The environment variable to set
            value: The value to set it to
        """
        self._default_env[key] = value

    def add_default_envmod(self, envmod: EnvironmentModifications) -> None:
        """Set an :class:`spack.util.environment.EnvironmentModifications` to use when the command
        is run."""
        self._default_envmod.extend(envmod)

    @property
    def command(self) -> str:
        """Returns the entire command-line string"""
        return " ".join(self.exe)

    @property
    def name(self) -> str:
        """Returns the executable name"""
        return PurePath(self.path).name

    @property
    def path(self) -> str:
        """Returns the executable path"""
        return str(PurePath(self.exe[0]))

    @overload
    def __call__(
        self,
        *args: str,
        fail_on_error: bool = ...,
        ignore_errors: Union[int, Sequence[int]] = ...,
        ignore_quotes: Optional[bool] = ...,
        timeout: Optional[int] = ...,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        input: Optional[BinaryIO] = ...,
        output: Union[Optional[BinaryIO], str] = ...,
        error: Union[Optional[BinaryIO], str] = ...,
        _dump_env: Optional[Dict[str, str]] = ...,
    ) -> None: ...

    @overload
    def __call__(
        self,
        *args: str,
        fail_on_error: bool = ...,
        ignore_errors: Union[int, Sequence[int]] = ...,
        ignore_quotes: Optional[bool] = ...,
        timeout: Optional[int] = ...,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        input: Optional[BinaryIO] = ...,
        output: Union[Type[str], Callable],  # str or str.split
        error: OutType = ...,
        _dump_env: Optional[Dict[str, str]] = ...,
    ) -> str: ...

    @overload
    def __call__(
        self,
        *args: str,
        fail_on_error: bool = ...,
        ignore_errors: Union[int, Sequence[int]] = ...,
        ignore_quotes: Optional[bool] = ...,
        timeout: Optional[int] = ...,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        input: Optional[BinaryIO] = ...,
        output: OutType = ...,
        error: Union[Type[str], Callable],  # str or str.split
        _dump_env: Optional[Dict[str, str]] = ...,
    ) -> str: ...

    def __call__(
        self,
        *args: str,
        fail_on_error: bool = True,
        ignore_errors: Union[int, Sequence[int]] = (),
        ignore_quotes: Optional[bool] = None,
        timeout: Optional[int] = None,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = None,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = None,
        input: Optional[BinaryIO] = None,
        output: OutType = None,
        error: OutType = None,
        _dump_env: Optional[Dict[str, str]] = None,
    ) -> Optional[str]:
        """Runs this executable in a subprocess.

        Parameters:
            *args: command-line arguments to the executable to run
            fail_on_error: if True, raises an exception if the subprocess returns an error
                The return code is available as :attr:`returncode`
            ignore_errors: a sequence of error codes to ignore. If these codes are returned, this
                process will not raise an exception, even if ``fail_on_error`` is set to ``True``
            ignore_quotes: if False, warn users that quotes are not needed, as Spack does not
                use a shell. If None, use :attr:`ignore_quotes`.
            timeout: the number of seconds to wait before killing the child process
            env: the environment with which to run the executable
            extra_env: extra items to add to the environment (neither requires nor precludes env)
            input: where to read stdin from
            output: where to send stdout
            error: where to send stderr
            _dump_env: dict to be set to the environment actually used (envisaged for
                testing purposes only)

        Accepted values for ``input``, ``output``, and ``error``:

        * Python streams: open Python file objects or ``os.devnull``
        * :obj:`str`: the Python string **type**. If you set these to :obj:`str`,
          output and error will be written to pipes and returned as a string.
          If both ``output`` and ``error`` are set to :obj:`str`, then one string
          is returned containing output concatenated with error. Not valid
          for ``input``.
        * :obj:`str.split`: the split method of the Python string type.
          Behaves the same as :obj:`str`, except that value is also written to
          ``stdout`` or ``stderr``.

        For ``output`` and ``error`` it's also accepted to pass a string with a filename, which
        will be automatically opened for writing.

        By default, the subprocess inherits the parent's file descriptors.
        """
        # Setup default environment
        current_environment = os.environ.copy() if env is None else {}
        self._default_envmod.apply_modifications(current_environment)
        current_environment.update(self._default_env)

        # Apply env argument
        if isinstance(env, EnvironmentModifications):
            env.apply_modifications(current_environment)
        elif env:
            current_environment.update(env)

        # Apply extra env
        if isinstance(extra_env, EnvironmentModifications):
            extra_env.apply_modifications(current_environment)
        elif extra_env is not None:
            current_environment.update(extra_env)

        if _dump_env is not None:
            _dump_env.clear()
            _dump_env.update(current_environment)

        if ignore_quotes is None:
            ignore_quotes = self.ignore_quotes

        # If they just want to ignore one error code, make it a tuple.
        if isinstance(ignore_errors, int):
            ignore_errors = (ignore_errors,)

        if input is str or input is str.split:
            raise ValueError("Cannot use `str` or `str.split` as input stream.")
        elif isinstance(input, str):
            istream, close_istream = open(input, "rb"), True
        else:
            istream, close_istream = input, False

        ostream, close_ostream = _streamify_output(output, "output")
        estream, close_estream = _streamify_output(error, "error")

        if not ignore_quotes:
            quoted_args = [arg for arg in args if re.search(r'^".*"$|^\'.*\'$', arg)]
            if quoted_args:
                tty.warn(
                    "Quotes in command arguments can confuse scripts like configure.",
                    "The following arguments may cause problems when executed:",
                    str("\n".join(["    " + arg for arg in quoted_args])),
                    "Quotes aren't needed because spack doesn't use a shell. "
                    "Consider removing them.",
                    "If multiple levels of quotation are required, use `ignore_quotes=True`.",
                )

        cmd = self.exe + list(args)

        cmd_line_string = " ".join(shlex.quote(arg) for arg in cmd)
        tty.debug(cmd_line_string)

        result = None
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=istream,
                stderr=estream,
                stdout=ostream,
                env=current_environment,
                close_fds=False,
            )
        except OSError as e:
            message = "Command: " + cmd_line_string
            if " " in self.exe[0]:
                message += "\nDid you mean to add a space to the command?"

            raise ProcessError(f"{self.exe[0]}: {e.strerror}", message)

        try:
            out, err = proc.communicate(timeout=timeout)
            result = _process_cmd_output(out, err, output, error)
            rc = self.returncode = proc.returncode
            if fail_on_error and rc != 0 and (rc not in ignore_errors):
                long_msg = cmd_line_string
                if result:
                    # If the output is not captured in the result, it will have
                    # been stored either in the specified files (e.g. if
                    # 'output' specifies a file) or written to the parent's
                    # stdout/stderr (e.g. if 'output' is not specified)
                    long_msg += "\n" + result

                raise ProcessError(f"Command exited with status {proc.returncode}:", long_msg)

        except subprocess.TimeoutExpired as te:
            proc.kill()
            out, err = proc.communicate()
            result = _process_cmd_output(out, err, output, error)
            long_msg = cmd_line_string + f"\n{result}"
            if fail_on_error:
                raise ProcessTimeoutError(
                    f"\nProcess timed out after {timeout}s. "
                    "We expected the following command to run quickly but it did not, "
                    f"please report this as an issue: {long_msg}",
                    long_message=long_msg,
                ) from te

        finally:
            # The isinstance checks are only needed for type checking.
            if close_ostream and isinstance(ostream, io.IOBase):
                ostream.close()
            if close_estream and isinstance(estream, io.IOBase):
                estream.close()
            if close_istream and isinstance(istream, io.IOBase):
                istream.close()

        return result

    def __eq__(self, other):
        return hasattr(other, "exe") and self.exe == other.exe

    def __hash__(self):
        return hash((type(self),) + tuple(self.exe))

    def __repr__(self):
        return f"<exe: {self.exe}>"

    def __str__(self):
        return " ".join(self.exe)


@overload
def which_string(
    *args: str, path: Optional[Union[List[str], str]] = ..., required: Literal[True]
) -> str: ...


@overload
def which_string(
    *args: str, path: Optional[Union[List[str], str]] = ..., required: bool = ...
) -> Optional[str]: ...


def which_string(
    *args: str, path: Optional[Union[List[str], str]] = None, required: bool = False
) -> Optional[str]:
    """Like :func:`which`, but returns a string instead of an :class:`Executable`."""
    if path is None:
        path = os.environ.get("PATH", "")

    if isinstance(path, list):
        paths = [Path(str(x)) for x in path]

    if isinstance(path, str):
        paths = [Path(x) for x in path.split(os.pathsep)]

    def get_candidate_items(search_item):
        if sys.platform == "win32" and not search_item.suffix:
            return [search_item.parent / (search_item.name + ext) for ext in [".exe", ".bat"]]

        return [Path(search_item)]

    def add_extra_search_paths(paths):
        with_parents = []
        with_parents.extend(paths)
        if sys.platform == "win32":
            for p in paths:
                if p.name == "bin":
                    with_parents.append(p.parent)
        return with_parents

    for search_item in args:
        search_paths = []
        search_paths.extend(paths)
        if search_item.startswith("."):
            # we do this because pathlib will strip any leading ./
            search_paths.insert(0, Path.cwd())
        search_paths = add_extra_search_paths(search_paths)

        candidate_items = get_candidate_items(Path(search_item))

        for candidate_item in candidate_items:
            for directory in search_paths:
                exe = directory / candidate_item
                try:
                    if exe.is_file() and os.access(str(exe), os.X_OK):
                        return str(exe)
                except OSError:
                    pass

    if required:
        raise CommandNotFoundError(f"spack requires '{args[0]}'. Make sure it is in your path.")

    return None


@overload
def which(
    *args: str, path: Optional[Union[List[str], str]] = ..., required: Literal[True]
) -> Executable: ...


@overload
def which(
    *args: str, path: Optional[Union[List[str], str]] = ..., required: bool = ...
) -> Optional[Executable]: ...


def which(
    *args: str, path: Optional[Union[List[str], str]] = None, required: bool = False
) -> Optional[Executable]:
    """Finds an executable in the path like command-line which.

    If given multiple executables, returns the first one that is found.
    If no executables are found, returns None.

    Parameters:
        *args: one or more executables to search for
        path: the path to search. Defaults to ``PATH``
        required: if set to :data:`True`, raise an error if executable not found

    Returns:
        The first executable that is found in the path or :data:`None` if not found.
    """
    exe = which_string(*args, path=path, required=required)
    return Executable(exe) if exe is not None else None


class ProcessError(spack.error.SpackError):
    """Raised when :class:`Executable` exits with an error code."""


class ProcessTimeoutError(ProcessError):
    """Raised when :class:`Executable` calls with a specified timeout exceed that time."""


class CommandNotFoundError(spack.error.SpackError):
    """Raised when :func:`which()` can't find a required executable."""
