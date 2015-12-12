##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
__all__ = ['Executable', 'which', 'ProcessError']

import os
import sys
import re
import subprocess
import inspect

import llnl.util.tty as tty
import spack
import spack.error


class Executable(object):
    """Class representing a program that can be run on the command line."""
    def __init__(self, name):
        self.exe = name.split(' ')
        self.returncode = None

        if not self.exe:
            raise ProcessError("Cannot construct executable for '%s'" % name)


    def add_default_arg(self, arg):
        self.exe.append(arg)


    @property
    def command(self):
        return ' '.join(self.exe)


    def __call__(self, *args, **kwargs):
        """Run the executable with subprocess.check_output, return output."""
        return_output = kwargs.get("return_output", False)
        fail_on_error = kwargs.get("fail_on_error", True)
        ignore_errors = kwargs.get("ignore_errors", ())

        output        = kwargs.get("output", sys.stdout)
        error         = kwargs.get("error", sys.stderr)
        input         = kwargs.get("input", None)

        def streamify(arg, mode):
            if isinstance(arg, basestring):
                return open(arg, mode), True
            elif arg is None and mode != 'r':
                return open(os.devnull, mode), True
            return arg, False
        output, ostream = streamify(output, 'w')
        error,  estream = streamify(error,  'w')
        input,  istream = streamify(input,  'r')

        # if they just want to ignore one error code, make it a tuple.
        if isinstance(ignore_errors, int):
            ignore_errors = (ignore_errors,)

        quoted_args = [arg for arg in args if re.search(r'^"|^\'|"$|\'$', arg)]
        if quoted_args:
            tty.warn("Quotes in command arguments can confuse scripts like configure.",
                     "The following arguments may cause problems when executed:",
                     str("\n".join(["    "+arg for arg in quoted_args])),
                     "Quotes aren't needed because spack doesn't use a shell.",
                     "Consider removing them")

        cmd = self.exe + list(args)

        cmd_line = ' '.join(cmd)
        tty.debug(cmd_line)

        try:
            proc = subprocess.Popen(
                cmd,
                stdin=input,
                stderr=error,
                stdout=subprocess.PIPE if return_output else output)
            out, err = proc.communicate()
            self.returncode = proc.returncode

            rc = proc.returncode
            if fail_on_error and rc != 0 and (rc not in ignore_errors):
                raise ProcessError("Command exited with status %d:"
                                   % proc.returncode, cmd_line)
            if return_output:
                return out

        except OSError, e:
            raise ProcessError(
                "%s: %s" % (self.exe[0], e.strerror),
                "Command: " + cmd_line)

        except subprocess.CalledProcessError, e:
            if fail_on_error:
                raise ProcessError(
                    str(e),
                    "\nExit status %d when invoking command: %s"
                    % (proc.returncode, cmd_line))

        finally:
            if ostream: output.close()
            if estream: error.close()
            if istream: input.close()


    def __eq__(self, other):
        return self.exe == other.exe


    def __neq__(self, other):
        return not (self == other)


    def __hash__(self):
        return hash((type(self),) + tuple(self.exe))


    def __repr__(self):
        return "<exe: %s>" % self.exe


    def __str__(self):
        return ' '.join(self.exe)



def which(name, **kwargs):
    """Finds an executable in the path like command-line which."""
    path     = kwargs.get('path', os.environ.get('PATH', '').split(os.pathsep))
    required = kwargs.get('required', False)

    if not path:
        path = []

    for dir in path:
        exe = os.path.join(dir, name)
        if os.path.isfile(exe) and os.access(exe, os.X_OK):
            return Executable(exe)

    if required:
        tty.die("spack requires %s.  Make sure it is in your path." % name)
    return None


class ProcessError(spack.error.SpackError):
    def __init__(self, msg, long_message=None):
        # These are used for detailed debugging information for
        # package builds.  They're built up gradually as the exception
        # propagates.
        self.package_context = _get_package_context()
        self.build_log = None

        super(ProcessError, self).__init__(msg, long_message)

    @property
    def long_message(self):
        msg = self._long_message
        if msg: msg += "\n\n"

        if self.build_log:
            msg += "See build log for details:\n"
            msg += "  %s" % self.build_log

        if self.package_context:
            if msg: msg += "\n\n"
            msg += '\n'.join(self.package_context)

        return msg


def _get_package_context():
    """Return some context for an error message when the build fails.

    This should be called within a ProcessError when the exception is
    thrown.

    Args:
    process_error -- A ProcessError raised during install()

    This function inspects the stack to find where we failed in the
    package file, and it adds detailed context to the long_message
    from there.

    """
    lines = []

    # Walk up the stack
    for f in inspect.stack():
        frame = f[0]

        # Find a frame with 'self' in the local variables.
        if not 'self' in frame.f_locals:
            continue

        # Look only at a frame in a subclass of spack.Package
        obj = frame.f_locals['self']
        if type(obj) != spack.Package and isinstance(obj, spack.Package):
            break
    else:
        # Didn't find anything
        return lines

    # Build a message showing where in install we failed.
    lines.append("%s:%d, in %s:" % (
        inspect.getfile(frame.f_code),
        frame.f_lineno,
        frame.f_code.co_name))

    sourcelines, start = inspect.getsourcelines(frame)
    for i, line in enumerate(sourcelines):
        mark = ">> " if start + i == frame.f_lineno else "   "
        lines.append("  %s%-5d%s" % (mark, start + i, line.rstrip()))

    return lines
