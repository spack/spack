##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import re
import subprocess
from six import string_types
import sys

import llnl.util.tty as tty

import spack.error

__all__ = ['Executable', 'which', 'ProcessError']


class Executable(object):
    """Class representing a program that can be run on the command line."""

    def __init__(self, name):
        self.exe = name.split(' ')
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
            env (dict): The environment to run the executable with
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
        * ``str``, as in the Python string type. If you set these to ``str``,
          output and error will be written to pipes and returned as a string.
          If both ``output`` and ``error`` are set to ``str``, then one string
          is returned containing output concatenated with error. Not valid
          for ``input``

        By default, the subprocess inherits the parent's file descriptors.
        """
        # Environment
        env_arg = kwargs.get('env', None)
        if env_arg is None:
            env = os.environ.copy()
            env.update(self.default_env)
        else:
            env = self.default_env.copy()
            env.update(env_arg)

        fail_on_error = kwargs.pop('fail_on_error', True)
        ignore_errors = kwargs.pop('ignore_errors', ())

        # If they just want to ignore one error code, make it a tuple.
        if isinstance(ignore_errors, int):
            ignore_errors = (ignore_errors, )

        input  = kwargs.pop('input',  None)
        output = kwargs.pop('output', None)
        error  = kwargs.pop('error',  None)

        if input is str:
            raise ValueError('Cannot use `str` as input stream.')

        def streamify(arg, mode):
            if isinstance(arg, string_types):
                return open(arg, mode), True
            elif arg is str:
                return subprocess.PIPE, False
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

        try:
            proc = subprocess.Popen(
                cmd,
                stdin=istream,
                stderr=estream,
                stdout=ostream,
                env=env)
            out, err = proc.communicate()

            rc = self.returncode = proc.returncode
            if fail_on_error and rc != 0 and (rc not in ignore_errors):
                raise ProcessError('Command exited with status %d:' %
                                   proc.returncode, cmd_line)

            if output is str or error is str:
                result = ''
                if output is str:
                    result += to_str(out)
                if error is str:
                    result += to_str(err)
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
        return self.exe == other.exe

    def __neq__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((type(self), ) + tuple(self.exe))

    def __repr__(self):
        return '<exe: %s>' % self.exe

    def __str__(self):
        return ' '.join(self.exe)


def to_str(content):
    """Produce a str type from the content of a process stream obtained with
       Popen.communicate.
    """
    # Prior to python3, Popen.communicate returns a str type. For python3 it
    # returns a bytes type. In the case of python3 we decode the
    # byte string to produce a str type. This will generate junk if the
    # encoding is not UTF-8 (which includes ASCII).
    if sys.version_info < (3, 0, 0):
        return content
    else:
        return content.decode('utf-8')


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
    path = kwargs.get('path', os.environ.get('PATH', ''))
    required = kwargs.get('required', False)

    if isinstance(path, string_types):
        path = path.split(os.pathsep)

    for name in args:
        for directory in path:
            exe = os.path.join(directory, name)
            if os.path.isfile(exe) and os.access(exe, os.X_OK):
                return Executable(exe)

    if required:
        tty.die("spack requires '%s'. Make sure it is in your path." % args[0])

    return None


class ProcessError(spack.error.SpackError):
    """ProcessErrors are raised when Executables exit with an error code."""
