# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utility classes for logging the output of blocks of code.
"""
from __future__ import unicode_literals

import multiprocessing
import os
import re
import select
import sys
import traceback
import signal
from contextlib import contextmanager
from six import string_types
from six import StringIO

import llnl.util.tty as tty

try:
    import termios
except ImportError:
    termios = None

# Use this to strip escape sequences
_escape = re.compile(r'\x1b[^m]*m|\x1b\[?1034h')

# control characters for enabling/disabling echo
#
# We use control characters to ensure that echo enable/disable are inline
# with the other output.  We always follow these with a newline to ensure
# one per line the following newline is ignored in output.
xon, xoff = '\x11\n', '\x13\n'
control = re.compile('(\x11\n|\x13\n)')


@contextmanager
def background_safe():
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)
    yield
    signal.signal(signal.SIGTTOU, signal.SIG_DFL)


def _is_background_tty():
    """Return True iff this process is backgrounded and stdout is a tty"""
    if sys.stdout.isatty():
        return os.getpgrp() != os.tcgetpgrp(sys.stdout.fileno())
    return False  # not writing to tty, not background


def _strip(line):
    """Strip color and control characters from a line."""
    return _escape.sub('', line)


class _keyboard_input(object):
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

        Note that stream can be None, in which case ``keyboard_input``
        will do nothing.
        """
        self.stream = stream

    def __enter__(self):
        """Enable immediate keypress input on stream.

        If the stream is not a TTY or the system doesn't support termios,
        do nothing.
        """
        self.old_cfg = None

        # Ignore all this if the input stream is not a tty.
        if not self.stream or not self.stream.isatty():
            return

        # If this fails, self.old_cfg will remain None
        if termios and not _is_background_tty():
            # save old termios settings
            old_cfg = termios.tcgetattr(self.stream)

            try:
                # create new settings with canonical input and echo
                # disabled, so keypresses are immediate & don't echo.
                self.new_cfg = termios.tcgetattr(self.stream)
                self.new_cfg[3] &= ~termios.ICANON
                self.new_cfg[3] &= ~termios.ECHO

                # Apply new settings for terminal
                termios.tcsetattr(self.stream, termios.TCSADRAIN, self.new_cfg)
                self.old_cfg = old_cfg

            except Exception:
                pass  # some OS's do not support termios, so ignore

    def __exit__(self, exc_type, exception, traceback):
        """If termios was avaialble, restore old settings."""
        if self.old_cfg:
            with background_safe():  # change it back even if backgrounded now
                termios.tcsetattr(self.stream, termios.TCSADRAIN, self.old_cfg)


class Unbuffered(object):
    """Wrapper for Python streams that forces them to be unbuffered.

    This is implemented by forcing a flush after each write.
    """
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def _file_descriptors_work(*streams):
    """Whether we can get file descriptors for the streams specified.

    This tries to call ``fileno()`` on all streams in the argument list,
    and returns ``False`` if anything goes wrong.

    This can happen, when, e.g., the test framework replaces stdout with
    a ``StringIO`` object.

    We have to actually try this to see whether it works, rather than
    checking for the fileno attribute, beacuse frameworks like pytest add
    dummy fileno methods on their dummy file objects that return
    ``UnsupportedOperationErrors``.

    """
    # test whether we can get fds for out and error
    try:
        for stream in streams:
            stream.fileno()
        return True
    except BaseException:
        return False


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
    ``force_echo``::

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

    def __init__(self, file_like=None, echo=False, debug=False, buffer=False):
        """Create a new output log context manager.

        Args:
            file_like (str or stream): open file object or name of file where
                output should be logged
            echo (bool): whether to echo output in addition to logging it
            debug (bool): whether to enable tty debug mode during logging
            buffer (bool): pass buffer=True to skip unbuffering output; note
                this doesn't set up any *new* buffering

        log_output can take either a file object or a filename. If a
        filename is passed, the file will be opened and closed entirely
        within ``__enter__`` and ``__exit__``. If a file object is passed,
        this assumes the caller owns it and will close it.

        By default, we unbuffer sys.stdout and sys.stderr because the
        logger will include output from executed programs and from python
        calls.  If stdout and stderr are buffered, their output won't be
        printed in the right place w.r.t. output from commands.

        Logger daemon is not started until ``__enter__()``.

        """
        self.file_like = file_like
        self.echo = echo
        self.debug = debug
        self.buffer = buffer

        self._active = False  # used to prevent re-entry

    def __call__(self, file_like=None, echo=None, debug=None, buffer=None):
        """Thie behaves the same as init. It allows a logger to be reused.

        Arguments are the same as for ``__init__()``.  Args here take
        precedence over those passed to ``__init__()``.

        With the ``__call__`` function, you can save state between uses
        of a single logger.  This is useful if you want to remember,
        e.g., the echo settings for a prior ``with log_output()``::

            logger = log_output()

            with logger('foo.txt'):
                # log things; user can change echo settings with 'v'

            with logger('bar.txt'):
                # log things; logger remembers prior echo settings.

        """
        if file_like is not None:
            self.file_like = file_like
        if echo is not None:
            self.echo = echo
        if debug is not None:
            self.debug = debug
        if buffer is not None:
            self.buffer = buffer
        return self

    def __enter__(self):
        if self._active:
            raise RuntimeError("Can't re-enter the same log_output!")

        if self.file_like is None:
            raise RuntimeError(
                "file argument must be set by either __init__ or __call__")

        # set up a stream for the daemon to write to
        self.close_log_in_parent = True
        self.write_log_in_parent = False
        if isinstance(self.file_like, string_types):
            self.log_file = open(self.file_like, 'w')

        elif _file_descriptors_work(self.file_like):
            self.log_file = self.file_like
            self.close_log_in_parent = False

        else:
            self.log_file = StringIO()
            self.write_log_in_parent = True

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

        # Multiprocessing pipe for communication back from the daemon
        # Currently only used to save echo value between uses
        self.parent, self.child = multiprocessing.Pipe()

        # Sets a daemon that writes to file what it reads from a pipe
        try:
            # need to pass this b/c multiprocessing closes stdin in child.
            try:
                input_stream = os.fdopen(os.dup(sys.stdin.fileno()))
            except BaseException:
                input_stream = None  # just don't forward input if this fails

            self.process = multiprocessing.Process(
                target=self._writer_daemon, args=(input_stream,))
            self.process.daemon = True  # must set before start()
            self.process.start()
            os.close(self.read_fd)  # close in the parent process

        finally:
            if input_stream:
                input_stream.close()

        # Flush immediately before redirecting so that anything buffered
        # goes to the original stream
        sys.stdout.flush()
        sys.stderr.flush()

        # Now do the actual output rediction.
        self.use_fds = _file_descriptors_work(sys.stdout, sys.stderr)
        if self.use_fds:
            # We try first to use OS-level file descriptors, as this
            # redirects output for subprocesses and system calls.

            # Save old stdout and stderr file descriptors
            self._saved_stdout = os.dup(sys.stdout.fileno())
            self._saved_stderr = os.dup(sys.stderr.fileno())

            # redirect to the pipe we created above
            os.dup2(self.write_fd, sys.stdout.fileno())
            os.dup2(self.write_fd, sys.stderr.fileno())
            os.close(self.write_fd)

        else:
            # Handle I/O the Python way. This won't redirect lower-level
            # output, but it's the best we can do, and the caller
            # shouldn't expect any better, since *they* have apparently
            # redirected I/O the Python way.

            # Save old stdout and stderr file objects
            self._saved_stdout = sys.stdout
            self._saved_stderr = sys.stderr

            # create a file object for the pipe; redirect to it.
            pipe_fd_out = os.fdopen(self.write_fd, 'w')
            sys.stdout = pipe_fd_out
            sys.stderr = pipe_fd_out

        # Unbuffer stdout and stderr at the Python level
        if not self.buffer:
            sys.stdout = Unbuffered(sys.stdout)
            sys.stderr = Unbuffered(sys.stderr)

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

        # print log contents in parent if needed.
        if self.write_log_in_parent:
            string = self.parent.recv()
            self.file_like.write(string)

        if self.close_log_in_parent:
            self.log_file.close()

        # recover and store echo settings from the child before it dies
        self.echo = self.parent.recv()

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

        # list of streams to select from
        istreams = [in_pipe, stdin] if stdin else [in_pipe]

        log_file = self.log_file

        def handle_write(force_echo):
            # Handle output from the with block process.
            # If we arrive here it means that in_pipe was
            # ready for reading : it should never happen that
            # line is false-ish
            line = in_pipe.readline()
            if not line:
                return (True, force_echo)  # break while loop

            # find control characters and strip them.
            controls = control.findall(line)
            line = re.sub(control, '', line)

            # Echo to stdout if requested or forced
            if echo or force_echo:
                try:
                    if termios:
                        conf = termios.tcgetattr(sys.stdout)
                        tostop = conf[3] & termios.TOSTOP
                    else:
                        tostop = True
                except Exception:
                    tostop = True
                if not (tostop and _is_background_tty()):
                    sys.stdout.write(line)
                    sys.stdout.flush()

            # Stripped output to log file.
            log_file.write(_strip(line))
            log_file.flush()

            if xon in controls:
                force_echo = True
            if xoff in controls:
                force_echo = False
            return (False, force_echo)

        try:
            with _keyboard_input(stdin):
                while True:
                    # No need to set any timeout for select.select
                    # Wait until a key press or an event on in_pipe.
                    rlist, _, _ = select.select(istreams, [], [])
                    # Allow user to toggle echo with 'v' key.
                    # Currently ignores other chars.
                    # only read stdin if we're in the foreground
                    if stdin in rlist and not _is_background_tty():
                        if stdin.read(1) == 'v':
                            echo = not echo

                    if in_pipe in rlist:
                        br, fe = handle_write(force_echo)
                        force_echo = fe
                        if br:
                            break

        except BaseException:
            tty.error("Exception occurred in writer daemon!")
            traceback.print_exc()

        finally:
            # send written data back to parent if we used a StringIO
            if self.write_log_in_parent:
                self.child.send(log_file.getvalue())
            log_file.close()

        # send echo value back to the parent so it can be preserved.
        self.child.send(echo)
