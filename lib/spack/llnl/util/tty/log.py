##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
"""Utility classes for logging the output of blocks of code.
"""
import multiprocessing
import os
import re
import select
import sys
from contextlib import contextmanager

import llnl.util.tty as tty

# Use this to strip escape sequences
_escape = re.compile(r'\x1b[^m]*m|\x1b\[?1034h')

# control characters for enabling/disabling echo
#
# We use control characters to ensure that echo enable/disable are inline
# with the other output.  We always follow these with a newline to ensure
# one per line the following newline is ignored in output.
xon, xoff = '\x11\n', '\x13\n'
control = re.compile('(\x11\n|\x13\n)')

def _strip(line):
    """Strip color and control characters from a line."""
    return _escape.sub('', line)


class keyboard_input(object):
    """Context manager to disable line editing and echoing.

    Use this with ``sys.stdin`` for keyboard input, e.g.::

        with keyboard_input(sys.stdin):
            r, w, x = select.select([sys.stdin], [], [])
            # ... do something with keypresses ...

    This disables canonical input so that keypresses are available on the
    stream immediately. Typically standard input allows line editing,
    which means keypresses won't be sent until the user hits return.

    It also disables echoing, so that keys pressed aren't printed to the
    terminal.  So, the user can hit, e.g., 'v', and it's read on the
    other end of the pipe immediately but not printed.

    When the with block completes, prior TTY settings are restored.

    Note: this depends on termios support.  If termios isn't available,
    or if the stream isn't a TTY, this context manager has no effect.
    """
    def __init__(self, stream):
        """Create a context manager that will enable keyboard input on stream.

        Args:
            stream (file-like): stream on which to accept keyboard input
        """
        self.stream = stream

    def __enter__(self):
        """Enable immediate keypress input on stream.

        If the stream is not a TTY or the system doesn't support termios,
        do nothing.
        """
        self.old_cfg = None

        # Ignore all this if the input stream is not a tty.
        if not self.stream.isatty():
            return

        try:
            # If this fails, self.old_cfg will remain None
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
            pass  # some OS's do not support termios, so ignore

    def __exit__(self, exc_type, exception, traceback):
        """If termios was avaialble, restore old settings."""
        if self.old_cfg:
            import termios
            termios.tcsetattr(
                self.stream.fileno(), termios.TCSADRAIN, self.old_cfg)


class log_output(object):
    """Context manager that logs its output to a file.

    In the simplest case, the usage looks like this::

        with log_output('logfile.txt'):
            # do things ... output will be logged

    Any output from the with block will be redirected to ``logfile.txt``.
    If you also want the output to be echoed to ``stdout``, use the
    ``echo`` parameter::

        with log_output('logfile.txt', echo=True):
            # do things ... output will be logged and printed out

    And, if you just want to echo *some* stuff from the parent, use
    ``force_echo``:

        with log_output('logfile.txt', echo=False) as logger:
            # do things ... output will be logged

            with logger.force_echo():
                # things here will be echoed *and* logged

    Under the hood, we spawn a daemon and set up a pipe between this
    process and the daemon.  The daemon writes our output to both the
    file and to stdout (if echoing).  The parent process can communicate
    with the daemon to tell it when and when not to echo; this is what
    force_echo does.  You can also enable/disable echoing by typing 'v'.

    We try to use OS-level file descriptors to do the redirection, but if
    stdout or stderr has been set to some Python-level file object, we
    use Python-level redirection instead.  This allows the redirection to
    work within test frameworks like nose and pytest.
    """

    def __init__(self, filename, echo=False, debug=False):
        """Create a new output log context manager.

        Logger daemon is not started until ``__enter__()``.
        """
        self.filename = filename
        self.echo = echo
        self.debug = debug

        self._active = False  # used to prevent re-entry

    def __enter__(self):
        if self._active:
            raise RuntimeError("Can't re-enter the same log_output!")

        # record parent color settings before redirecting.  We do this
        # because color output depends on whether the *original* stdout
        # is a TTY.  New stdout won't be a TTY so we force colorization.
        self._saved_color = tty.color._force_color
        forced_color = tty.color.get_color_when()

        # also record parent debug settings -- in case the logger is
        # forcing debug output.
        self._saved_debug = tty._debug

        # OS-level pipe for redirecting output to logger
        self.read_fd, self.write_fd = os.pipe()

        # Sets a daemon that writes to file what it reads from a pipe
        try:
            # need to pass this b/c multiprocessing closes stdin in child.
            input_stream = os.fdopen(os.dup(sys.stdin.fileno()))

            self.process = multiprocessing.Process(
                target=self._writer_daemon, args=(input_stream,))
            self.process.daemon = True  # must set before start()
            self.process.start()
            os.close(self.read_fd)  # close in the parent process

        finally:
            input_stream.close()

        # Flush immediately before redirecting so that anything buffered
        # goes to the original stream
        sys.stdout.flush()
        sys.stderr.flush()

        # Now do the actual output rediction.
        self.use_fds = True
        try:
            # We try first to use OS-level file descriptors, as this
            # redirects output for subprocesses and system calls.

            # Save old stdout and stderr file descriptors
            self._saved_stdout = os.dup(sys.stdout.fileno())
            self._saved_stderr = os.dup(sys.stderr.fileno())

            # redirect to the pipe we created above
            os.dup2(self.write_fd, sys.stdout.fileno())
            os.dup2(self.write_fd, sys.stderr.fileno())
            os.close(self.write_fd)

        except AttributeError:
            # Using file descriptors can fail if stdout and stderr don't
            # have a fileno attribute. This can happen, when, e.g., the
            # test framework replaces stdout with a StringIO object.  We
            # handle thi the Python way. This won't redirect lower-level
            # output, but it's the best we can do.
            self.use_fds = False

            # Save old stdout and stderr file objects
            self._saved_stdout = sys.stdout
            self._saved_stderr = sys.stderr

            # create a file object for the pipe; redirect to it.
            pipe_fd_out = os.fdopen(self.write_fd, 'w')
            sys.stdout = pipe_fd_out
            sys.stderr = pipe_fd_out

        # Force color and debug settings now that we have redirected.
        tty.color.set_color_when(forced_color)
        tty._debug = self.debug

        # track whether we're currently inside this log_output
        self._active = True

        # return this log_output object so that the user can do things
        # like temporarily echo some ouptut.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Flush any buffered output to the logger daemon.
        sys.stdout.flush()
        sys.stderr.flush()

        # restore previous output settings, either the low-level way or
        # the python way
        if self.use_fds:
            os.dup2(self._saved_stdout, sys.stdout.fileno())
            os.close(self._saved_stdout)

            os.dup2(self._saved_stderr, sys.stderr.fileno())
            os.close(self._saved_stderr)
        else:
            sys.stdout = self._saved_stdout
            sys.stderr = self._saved_stderr

        # join the daemon process. The daemon will quit automatically
        # when the write pipe is closed; we just wait for it here.
        self.process.join()

        # restore old color and debug settings
        tty.color._force_color = self._saved_color
        tty._debug = self._saved_debug

        self._active = False  # safe to enter again

    @contextmanager
    def force_echo(self):
        """Context manager to force local echo, even if echo is off."""
        if not self._active:
            raise RuntimeError(
                "Can't call force_echo() outside log_output region!")

        # This uses the xon/xoff to highlight regions to be echoed in the
        # output. We us these control characters rather than, say, a
        # separate pipe, because they're in-band and assured to appear
        # exactly before and after the text we want to echo.
        sys.stdout.write(xon)
        sys.stdout.flush()
        yield
        sys.stdout.write(xoff)
        sys.stdout.flush()

    def _writer_daemon(self, stdin):
        """Daemon that writes output to the log file and stdout."""
        # Use line buffering (3rd param = 1) since Python 3 has a bug
        # that prevents unbuffered text I/O.
        in_pipe = os.fdopen(self.read_fd, 'r', 1)
        os.close(self.write_fd)

        echo = self.echo        # initial echo setting, user-controllable
        force_echo = False      # parent can force echo for certain output

        with open(self.filename, 'w') as log_file:
            with keyboard_input(stdin):
                while True:
                    # Without the last parameter (timeout) select will
                    # wait until at least one of the two streams are
                    # ready. This may cause the function to hang.
                    rlist, _, xlist = select.select(
                        [in_pipe, stdin], [], [], 0)

                    # Allow user to toggle echo with 'v' key.
                    # Currently ignores other chars.
                    if stdin in rlist:
                        if stdin.read(1) == 'v':
                            echo = not echo

                    # Handle output from the with block process.
                    if in_pipe in rlist:
                        # If we arrive here it means that in_pipe was
                        # ready for reading : it should never happen that
                        # line is false-ish
                        line = in_pipe.readline()
                        if not line:
                            break  # EOF

                        # find control characters and strip them.
                        controls = control.findall(line)
                        line = re.sub(control, '', line)

                        # Echo to stdout if requested or forced
                        if echo or force_echo:
                            sys.stdout.write(line)

                        # Stripped output to log file.
                        log_file.write(_strip(line))
                        log_file.flush()

                        if xon in controls:
                            force_echo = True
                        if xoff in controls:
                            force_echo = False
