# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""The pty module handles pseudo-terminals.

Currently, the infrastructure here is only used to test llnl.util.tty.log.
"""
from __future__ import print_function

import os
import signal
import multiprocessing
import re
import sys
import termios
import time
import traceback

import llnl.util.tty.log as log

from spack.util.executable import which


class ProcessController(object):
    """Wrapper around some fundamental process control operations.

    This allows one process to drive another similar to the way a shell
    would, by sending signals and I/O.

    """
    def __init__(self, pid, master_fd, timeout=1, debug=False):
        """Create a controller to manipulate the process with id ``pid``

        Args:
            pid (int): id of process to control
            master_fd (int): master file descriptor created as with
                ``os.openpty()``, attached to pid's stdin
            timeout (int): time in seconds for wait operations to time out
                (default 1 second)
            debug (bool): whether ``hline()`` and ``status()`` should
                produce output when called (default False)

        """
        self.pid = pid
        self.pgid = os.getpgid(pid)
        self.master_fd = master_fd
        self.timeout = timeout
        self.debug = debug

        # we need the ps command to wait for process statuses
        self.ps = which("ps", required=True)

    def get_canon_echo_attrs(self):
        """Get echo and canon attributes of the terminal of master_fd."""
        cfg = termios.tcgetattr(self.master_fd)
        return (
            bool(cfg[3] & termios.ICANON),
            bool(cfg[3] & termios.ECHO),
        )

    def hline(self, name):
        """Labled horizontal line for debugging."""
        if self.debug:
            sys.stderr.write(
                "------------------------------------------- %s\n" % name
            )

    def status(self):
        """Print debug messgae with status info for the child."""
        if self.debug:
            canon, echo = self.get_canon_echo_attrs()
            sys.stderr.write("canon: %s, echo: %s\n" % (
                "on" if canon else "off",
                "on" if echo else "off",
            ))
            sys.stderr.write("input: %s\n" % self.input_on())
            sys.stderr.write("bg: %s\n" % self.background())
            sys.stderr.write("\n")

    def input_on(self):
        """True if the temrchild process """
        return self.get_canon_echo_attrs() == (False, False)

    def background(self):
        """True if pgid is in a background pgroup of master_fd's terminal."""
        return self.pgid != os.tcgetpgrp(self.master_fd)

    def tstp(self):
        """Send SIGTSTP to the controlled process."""
        self.hline("tstp")
        os.killpg(self.pgid, signal.SIGTSTP)

    def cont(self):
        self.hline("cont")
        os.killpg(self.pgid, signal.SIGCONT)

    def fg(self):
        self.hline("fg")
        os.tcsetpgrp(self.master_fd, os.getpgid(self.pid))

    def bg(self):
        self.hline("bg")
        with log.ignore_signal(signal.SIGTTOU):
            os.tcsetpgrp(self.master_fd, os.getpgrp())

    def write(self, byte_string):
        self.hline("write '%s'" % byte_string.decode("utf-8"))
        os.write(self.master_fd, byte_string)

    def wait(self, condition):
        start = time.time()
        while (((time.time() - start) < self.timeout) and not condition()):
            time.sleep(1e-2)
        assert condition()

    def wait_enabled(self):
        self.wait(lambda: self.input_on() and not self.background())

    def wait_disabled(self):
        self.wait(lambda: not self.input_on() and self.background())

    def wait_disabled_fg(self):
        self.wait(lambda: not self.input_on() and not self.background())

    def proc_status(self):
        status = self.ps("-p", str(self.pid), "-o", "stat", output=str)
        status = re.split(r"\s+", status.strip(), re.M)
        return status[1]

    def wait_stopped(self):
        self.wait(lambda: "T" in self.proc_status())

    def wait_running(self):
        status = self.proc_status()
        self.wait(lambda: "T" not in status)


def _child_process(
        tty_name, stdout_fd, stderr_fd, ready, child_function, attrs):
    """Child process wrapper for PseudoShell.

    Handles the mechanics of setting up a PTY, then calls
    ``child_function``.

    """
    # new process group, like a command or pipeline launched by a shell
    os.setpgrp()

    # take controlling terminal and set up pty IO
    stdin_fd = os.open(tty_name, os.O_RDWR)
    os.dup2(stdin_fd, sys.stdin.fileno())
    os.dup2(stdout_fd, sys.stdout.fileno())
    os.dup2(stderr_fd, sys.stderr.fileno())
    os.close(stdin_fd)

    if attrs.get("debug"):
        sys.stderr.write("child: stdin.isatty(): %s\n" % sys.stdin.isatty())

    # tell the parent that we're really running
    if attrs.get("debug"):
        sys.stderr.write("child: ready!\n")
    ready.value = True

    child_function(attrs)


def _master_process(master_function, child_function, attrs):
    """Master process wrapper for PseudoShell.

    Handles the mechanics of setting up a PTY, then calls
    ``master_function``.

    """
    os.setsid()   # new session; this process is the controller
    os.setpgrp()  # new process group for this process

    master_fd, child_fd = os.openpty()
    pty_name = os.ttyname(child_fd)
    with open(pty_name, "w+b"):
        pass  # take controlling terminal

    ready = multiprocessing.Value('i', False)
    proc = multiprocessing.Process(
        target=_child_process,
        args=(pty_name, sys.stdout.fileno(), sys.stderr.fileno(),
              ready, child_function, attrs)
    )
    proc.start()

    # wait for subprocess to be running and connected.
    while not ready.value:
        time.sleep(1e-5)
        pass

    if attrs.get("debug"):
        sys.stderr.write("pid:        %d\n" % os.getpid())
        sys.stderr.write("pgid:       %d\n" % os.getpgrp())
        sys.stderr.write("sid:        %d\n" % os.getsid(0))
        sys.stderr.write("tcgetpgrp:  %d\n" % os.tcgetpgrp(master_fd))
        sys.stderr.write("\n")

        proc_pgid = os.getpgid(proc.pid)
        sys.stderr.write("child pid:  %d\n" % proc.pid)
        sys.stderr.write("child pgid: %d\n" % proc_pgid)
        sys.stderr.write("child sid:  %d\n" % os.getsid(proc.pid))
        sys.stderr.write("\n")
        sys.stderr.flush()
    # set up master to ignore SIGTSTP, like a shell
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)

    # call the master function once the child is ready
    try:
        controller = ProcessController(
            proc.pid, master_fd, debug=attrs.get("debug"))
        error = master_function(proc, controller, attrs)
    except BaseException:
        error = 1
        traceback.print_exc()

    proc.join()

    return error or proc.exitcode


class PseudoShell(object):
    """Sets up master and child processes with a PTY.

    You can create a ``PseudoShell`` if you want to test how some
    function responds to terminal input.  This is a pseudo-shell from a
    job control perspective; ``master_function`` and ``child_function``
    are set up with a pseudoterminal (pty) so that the master can drive
    the child through process control signals and I/O.

    The two functions should have signatures like this::

        def master_function(proc, ctl, attrs)
        def child_function(attrs)

    ``master_function`` is spawned in its own process and passed three
    arguments:

      1. ``proc``, the ``multiprocessing.Process`` object
         representing the child;
      2. ``ctl``, a ``ProcessController`` object tied to the child; and
      3. ``attrs``, a ``dict`` object from ``multiprocessing.Manager``
         that can be used to share state among the caller, master, and
         child processes.

    ``child_function`` is only passed the ``attrs`` dictionary.

    The ``ctl.master_fd`` will have its ``master_fd`` connected to
    ``sys.stdin`` in the child process. Both processes will share the
    same ``sys.stdout`` and ``sys.stderr`` as the process instantiating
    ``PseudoShell``.

    """
    def __init__(self, master_function, child_function):
        self.proc = None
        self.master_function = master_function
        self.child_function = child_function

        # attrs can be used to pass parameters to master and child
        self.manager = multiprocessing.Manager()
        self.attrs = self.manager.dict()

    def start(self):
        """Start the master and child processes.

        The master process will create the child, then call
        ``master_function``.  The child process will call
        ``child_function``.
        """
        self.proc = multiprocessing.Process(
            target=_master_process,
            args=(self.master_function, self.child_function, self.attrs)
        )
        self.proc.start()

    def join(self):
        """Wait for the child process to finish, and return its exit code."""
        self.proc.join()
        return self.proc.exitcode
