# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys
import os
import re
import shlex
import subprocess
from six import string_types, text_type, StringIO

import llnl.util.tty as tty

import spack.error

__all__ = ['Executable', 'which', 'ProcessError']


class Executable(object):
    """Class representing a program that can be run on the command line."""

    def __init__(self, name):
        self.exe = shlex.split(str(name))
        self.default_env = {}
        self.returncode = None

        if not self.exe:
            raise ProcessError("Cannot construct executable for '%s'" % name)

    def add_default_arg(self, arg):
        """Add a default argument to the command."""
        self.exe.append(arg)

    def add_default_env(self, key, value):
        """Set an environment variable when the command is run.

        Parameters:
            key: The environment variable to set
            value: The value to set it to
        """
        self.default_env[key] = value

    @property
    def command(self):
        """The command-line string.

        Returns:
            str: The executable and default arguments
        """
        return ' '.join(self.exe)

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
            env (dict): The environment to run the executable with
            extra_env (dict): Extra items to add to the environment
                (neither requires nor precludes env)
            fail_on_error (bool): Raise an exception if the subprocess returns
                an error. Default is True. The return code is available as
                ``exe.returncode``
            ignore_errors (int or list): A list of error codes to ignore.
                If these codes are returned, this process will not raise
                an exception even if ``fail_on_error`` is set to ``True``
            input: Where to read stdin from
            output: Where to send stdout
            error: Where to send stderr

        Accepted values for input, output, and error:

        * python streams, e.g. open Python file objects, or ``os.devnull``
        * filenames, which will be automatically opened for writing

        By default, the subprocess inherits the parent's file descriptors.

        Returns:
            (str) The interleaved output and error
        """
        # Environment
        env_arg = kwargs.get('env', None)
        if env_arg is None:
            env = os.environ.copy()
            env.update(self.default_env)
        else:
            env = self.default_env.copy()
            env.update(env_arg)
        env.update(kwargs.get('extra_env', {}))
        if '_dump_env' in kwargs:
            kwargs['_dump_env'].clear()
            kwargs['_dump_env'].update(env)

        fail_on_error = kwargs.pop('fail_on_error', True)
        ignore_errors = kwargs.pop('ignore_errors', ())

        # If they just want to ignore one error code, make it a tuple.
        if isinstance(ignore_errors, int):
            ignore_errors = (ignore_errors, )

        input  = kwargs.pop('input',  None)
        output = kwargs.pop('output', sys.stdout)
        error  = kwargs.pop('error',  sys.stderr)

        if input is str:
            raise ValueError('Cannot use `str` as input stream.')

        if output is str:
            output = os.devnull
        if error is str:
            error = os.devnull

        def streamify(arg, mode):
            if isinstance(arg, string_types):
                return open(arg, mode), True
            else:
                return arg, False

        ostream, close_ostream = streamify(output, 'w')
        estream, close_estream = streamify(error,  'w')
        istream, close_istream = streamify(input,  'r')

        quoted_args = [arg for arg in args if re.search(r'^"|^\'|"$|\'$', arg)]
        if quoted_args:
            tty.warn(
                "Quotes in command arguments can confuse scripts like"
                " configure.",
                "The following arguments may cause problems when executed:",
                str("\n".join(["    " + arg for arg in quoted_args])),
                "Quotes aren't needed because spack doesn't use a shell.",
                "Consider removing them")

        cmd = self.exe + list(args)

        cmd_line = "'%s'" % "' '".join(
            map(lambda arg: arg.replace("'", "'\"'\"'"), cmd))

        tty.debug(cmd_line)

        output_string = StringIO()
        # Determine whether any of our streams are StringIO
        # We cannot call `Popen` directly with a StringIO object
        output_use_stringIO = False
        if not hasattr(ostream, 'fileno'):
            output_use_stringIO = True
            ostream_stringIO = ostream
            ostream = subprocess.PIPE
        error_use_stringIO = False
        if not hasattr(estream, 'fileno'):
            error_use_stringIO = True
            estream_stringIO = estream
            estream = subprocess.PIPE

        try:
            with tty.log.log_output(
                    output_string, output=ostream, error=estream, echo=True):
                proc = subprocess.Popen(
                    cmd,
                    stdin=istream,
                    stderr=estream,
                    stdout=ostream,
                    env=env)
                out, err = proc.communicate()

                if output_use_stringIO:
                    ostream_stringIO.write(out)
                if error_use_stringIO:
                    estream_stringIO.write(err)

            result = output_string.getvalue()

            rc = self.returncode = proc.returncode
            if fail_on_error and rc != 0 and (rc not in ignore_errors):
                long_msg = cmd_line
                if output == os.devnull or error == os.devnull:
                    # If the output is not being printed anywhere, include it
                    # in the error message. Otherwise, don't pollute the error
                    # message.
                    long_msg += '\n' + result

                raise ProcessError('Command exited with status %d:' %
                                   proc.returncode, long_msg)

            return result

        except OSError as e:
            raise ProcessError(
                '%s: %s' % (self.exe[0], e.strerror), 'Command: ' + cmd_line)

        except subprocess.CalledProcessError as e:
            if fail_on_error:
                raise ProcessError(
                    str(e), '\nExit status %d when invoking command: %s' %
                    (proc.returncode, cmd_line))

        finally:
            if close_ostream:
                ostream.close()
            if close_estream:
                estream.close()
            if close_istream:
                istream.close()

    def __eq__(self, other):
        return hasattr(other, 'exe') and self.exe == other.exe

    def __neq__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((type(self), ) + tuple(self.exe))

    def __repr__(self):
        return '<exe: %s>' % self.exe

    def __str__(self):
        return ' '.join(self.exe)


def which_string(*args, **kwargs):
    """Like ``which()``, but return a string instead of an ``Executable``."""
    path = kwargs.get('path', os.environ.get('PATH', ''))
    required = kwargs.get('required', False)

    if isinstance(path, string_types):
        path = path.split(os.pathsep)

    for name in args:
        if os.path.sep in name:
            exe = os.path.abspath(name)
            if os.path.isfile(exe) and os.access(exe, os.X_OK):
                return exe
        else:
            for directory in path:
                exe = os.path.join(directory, name)
                if os.path.isfile(exe) and os.access(exe, os.X_OK):
                    return exe

    if required:
        raise CommandNotFoundError(
            "spack requires '%s'. Make sure it is in your path." % args[0])

    return None


def which(*args, **kwargs):
    """Finds an executable in the path like command-line which.

    If given multiple executables, returns the first one that is found.
    If no executables are found, returns None.

    Parameters:
        *args (str): One or more executables to search for

    Keyword Arguments:
        path (:func:`list` or str): The path to search. Defaults to ``PATH``
        required (bool): If set to True, raise an error if executable not found

    Returns:
        Executable: The first executable that is found in the path
    """
    exe = which_string(*args, **kwargs)
    return Executable(exe) if exe else None


class ProcessError(spack.error.SpackError):
    """ProcessErrors are raised when Executables exit with an error code."""


class CommandNotFoundError(spack.error.SpackError):
    """Raised when ``which()`` can't find a required executable."""
