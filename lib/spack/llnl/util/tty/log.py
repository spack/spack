##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
"""Utility classes for logging the output of blocks of code.
"""
import multiprocessing
import os
import re
import select
import sys

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

        except Exception:
            pass  # Some OS's do not support termios, so ignore.

    def __exit__(self, exc_type, exception, traceback):
        # If termios was avaialble, restore old settings after the
        # with block
        if self.old_cfg:
            import termios
            termios.tcsetattr(
                self.stream.fileno(), termios.TCSADRAIN, self.old_cfg)


class log_output(object):
    """Spawns a daemon that reads from a pipe and writes to a file

    Usage:
        # Spawns the daemon
        with log_output('logfile.txt', 'w') as log_redirection:
           # do things ... output is not redirected
           with log_redirection:
                # do things ... output will be logged

    or:
        with log_output('logfile.txt', echo=True) as log_redirection:
           # do things ... output is not redirected
           with log_redirection:
               # do things ... output will be logged
               # and also printed to stdout.

    Opens a stream in 'w' mode at daemon spawning and closes it at
    daemon joining. If echo is True, also prints the output to stdout.
    """

    def __init__(
            self,
            filename,
            echo=False,
            force_color=False,
            debug=False,
            input_stream=sys.stdin
    ):
        self.filename = filename
        # Various output options
        self.echo = echo
        self.force_color = force_color
        self.debug = debug

        # Default is to try file-descriptor reassignment unless the system
        # out/err streams do not have an associated file descriptor
        self.directAssignment = False
        self.read, self.write = os.pipe()

        # Needed to un-summon the daemon
        self.parent_pipe, self.child_pipe = multiprocessing.Pipe()
        # Input stream that controls verbosity interactively
        self.input_stream = input_stream

    def __enter__(self):
        # Sets a daemon that writes to file what it reads from a pipe
        try:
            fwd_input_stream = os.fdopen(
                os.dup(self.input_stream.fileno())
            )
            self.p = multiprocessing.Process(
                target=self._spawn_writing_daemon,
                args=(self.read, fwd_input_stream),
                name='logger_daemon'
            )
            self.p.daemon = True
            self.p.start()
        finally:
            fwd_input_stream.close()
        return log_output.OutputRedirection(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.parent_pipe.send(True)
        self.p.join(60.0)  # 1 minute to join the child

    def _spawn_writing_daemon(self, read, input_stream):
        # Parent: read from child, skip the with block.
        read_file = os.fdopen(read, 'r', 0)
        with open(self.filename, 'w') as log_file:
            with keyboard_input(input_stream):
                while True:
                    # Without the last parameter (timeout) select will wait
                    # until at least one of the two streams are ready. This
                    # may cause the function to hang.
                    rlist, _, _ = select.select(
                        [read_file, input_stream], [], [], 0
                    )

                    # Allow user to toggle echo with 'v' key.
                    # Currently ignores other chars.
                    if input_stream in rlist:
                        if input_stream.read(1) == 'v':
                            self.echo = not self.echo

                    # Handle output from the with block process.
                    if read_file in rlist:
                        # If we arrive here it means that
                        # read_file was ready for reading : it
                        # should never happen that line is false-ish
                        line = read_file.readline()

                        # Echo to stdout if requested.
                        if self.echo:
                            sys.stdout.write(line)

                        # Stripped output to log file.
                        log_file.write(_strip(line))
                        log_file.flush()

                    if self.child_pipe.poll():
                        break

    def __del__(self):
        """Closes the pipes"""
        os.close(self.write)
        os.close(self.read)

    class OutputRedirection(object):

        def __init__(self, other):
            self.__dict__.update(other.__dict__)

        def __enter__(self):
            """Redirect output from the with block to a file.

            Hijacks stdout / stderr and writes to the pipe
            connected to the logger daemon
            """
            # remember these values for later.
            self._force_color = color._force_color
            self._debug = tty._debug
            # Redirect this output to a pipe
            write = self.write
            try:
                # Save old stdout and stderr
                self._stdout = os.dup(sys.stdout.fileno())
                self._stderr = os.dup(sys.stderr.fileno())

                # redirect to the pipe.
                os.dup2(write, sys.stdout.fileno())
                os.dup2(write, sys.stderr.fileno())
            except AttributeError:
                self.directAssignment = True
                self._stdout = sys.stdout
                self._stderr = sys.stderr
                output_redirect = os.fdopen(write, 'w')
                sys.stdout = output_redirect
                sys.stderr = output_redirect
            if self.force_color:
                color._force_color = True
            if self.debug:
                tty._debug = True

        def __exit__(self, exc_type, exception, traceback):
            """Plugs back the original file descriptors
            for stdout and stderr
            """
            # Flush the log to disk.
            sys.stdout.flush()
            sys.stderr.flush()
            if self.directAssignment:
                # We seem to need this only to pass test/install.py
                sys.stdout = self._stdout
                sys.stderr = self._stderr
            else:
                os.dup2(self._stdout, sys.stdout.fileno())
                os.dup2(self._stderr, sys.stderr.fileno())

            # restore output options.
            color._force_color = self._force_color
            tty._debug = self._debug
