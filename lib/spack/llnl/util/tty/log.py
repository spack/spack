##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
"""Utility classes for logging the output of blocks of code.
"""
import sys
import os
import re
import select
import inspect

import llnl.util.tty as tty
import llnl.util.tty.color as color

# Use this to strip escape sequences
_escape = re.compile(r'\x1b[^m]*m|\x1b\[?1034h')

def _strip(line):
    """Strip color and control characters from a line."""
    return _escape.sub('', line)


class _SkipWithBlock():
    """Special exception class used to skip a with block."""
    pass


class keyboard_input(object):
    """Disable canonical input and echo on a stream within a with block.

    Use this with sys.stdin for keyboard input, e.g.:

        with keyboard_input(sys.stdin):
            r, w, x = select.select([sys.stdin], [], [])
            # ... do something with keypresses ...

    When the with block completes, this will restore settings before
    canonical and echo were disabled.
    """
    def __init__(self, stream):
        self.stream = stream


    def __enter__(self):
        self.old_cfg = None

        # Ignore all this if the input stream is not a tty.
        if not self.stream.isatty():
            return

        try:
            # import and mark whether it worked.
            import termios

            # save old termios settings
            fd = self.stream.fileno()
            self.old_cfg = termios.tcgetattr(fd)

            # create new settings with canonical input and echo
            # disabled, so keypresses are immediate & don't echo.
            self.new_cfg = termios.tcgetattr(fd)
            self.new_cfg[3] &= ~termios.ICANON
            self.new_cfg[3] &= ~termios.ECHO

            # Apply new settings for terminal
            termios.tcsetattr(fd, termios.TCSADRAIN, self.new_cfg)

        except Exception, e:
            pass  # Some OS's do not support termios, so ignore.


    def __exit__(self, exc_type, exception, traceback):
        # If termios was avaialble, restore old settings after the
        # with block
        if self.old_cfg:
            import termios
            termios.tcsetattr(
                self.stream.fileno(), termios.TCSADRAIN, self.old_cfg)


class log_output(object):
    """Redirects output and error of enclosed block to a file.

    Usage:
        with log_output(open('logfile.txt', 'w')):
           # do things ... output will be logged.

    or:
        with log_output(open('logfile.txt', 'w'), echo=True):
           # do things ... output will be logged
           # and also printed to stdout.

    Closes the provided stream when done with the block.
    If echo is True, also prints the output to stdout.
    """
    def __init__(self, stream, echo=False, force_color=False, debug=False):
        self.stream = stream

        # various output options
        self.echo = echo
        self.force_color = force_color
        self.debug = debug

    def trace(self, frame, event, arg):
        """Jumps to __exit__ on the child process."""
        raise _SkipWithBlock()


    def __enter__(self):
        """Redirect output from the with block to a file.

        This forks the with block as a separate process, with stdout
        and stderr redirected back to the parent via a pipe.  If
        echo is set, also writes to standard out.

        """
        # remember these values for later.
        self._force_color = color._force_color
        self._debug = tty._debug

        read, write = os.pipe()

        self.pid = os.fork()
        if self.pid:
            # Parent: read from child, skip the with block.
            os.close(write)

            read_file = os.fdopen(read, 'r', 0)
            with self.stream as log_file:
                with keyboard_input(sys.stdin):
                    while True:
                        rlist, w, x = select.select([read_file, sys.stdin], [], [])
                        if not rlist:
                            break

                        # Allow user to toggle echo with 'v' key.
                        # Currently ignores other chars.
                        if sys.stdin in rlist:
                            if sys.stdin.read(1) == 'v':
                                self.echo = not self.echo

                        # handle output from the with block process.
                        if read_file in rlist:
                            line = read_file.readline()
                            if not line:
                                break

                            # Echo to stdout if requested.
                            if self.echo:
                                sys.stdout.write(line)

                            # Stripped output to log file.
                            log_file.write(_strip(line))

            read_file.flush()
            read_file.close()

            # Set a trace function to skip the with block.
            sys.settrace(lambda *args, **keys: None)
            frame = inspect.currentframe(1)
            frame.f_trace = self.trace

        else:
            # Child: redirect output, execute the with block.
            os.close(read)

            # Save old stdout and stderr
            self._stdout = os.dup(sys.stdout.fileno())
            self._stderr = os.dup(sys.stderr.fileno())

            # redirect to the pipe.
            os.dup2(write, sys.stdout.fileno())
            os.dup2(write, sys.stderr.fileno())

            if self.force_color:
                color._force_color = True

            if self.debug:
                tty._debug = True


    def __exit__(self, exc_type, exception, traceback):
        """Exits on child, handles skipping the with block on parent."""
        # Child should just exit here.
        if self.pid == 0:
            # Flush the log to disk.
            sys.stdout.flush()
            sys.stderr.flush()

            if exception:
                # Restore stdout on the child if there's an exception,
                # and let it be raised normally.
                #
                # This assumes that even if the exception is caught,
                # the child will exit with a nonzero return code.  If
                # it doesn't, the child process will continue running.
                #
                # TODO: think about how this works outside install.
                # TODO: ideally would propagate exception to parent...
                os.dup2(self._stdout, sys.stdout.fileno())
                os.dup2(self._stderr, sys.stderr.fileno())

                return False

            else:
                # Die quietly if there was no exception.
                os._exit(0)

        else:
            # If the child exited badly, parent also should exit.
            pid, returncode = os.waitpid(self.pid, 0)
            if returncode != 0:
                os._exit(1)

        # restore output options.
        color._force_color = self._force_color
        tty._debug = self._debug

        # Suppresses exception if it's our own.
        return exc_type is _SkipWithBlock
