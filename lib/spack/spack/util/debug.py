# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Debug signal handler: prints a stack trace and enters interpreter.

``register_interrupt_handler()`` enables a ctrl-C handler that prints
a stack trace and drops the user into an interpreter.

"""
import code
import os
import pdb
import signal
import sys
import traceback


def debug_handler(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d = {'_frame': frame}         # Allow access to frame object.
    d.update(frame.f_globals)    # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message  = "Signal received : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)
    os._exit(1)  # Use os._exit to avoid test harness.


def register_interrupt_handler():
    """Print traceback and enter an interpreter on Ctrl-C"""
    signal.signal(signal.SIGINT, debug_handler)


# Subclass of the debugger to keep readline working.  See
# https://stackoverflow.com/questions/4716533/how-to-attach-debugger-to-a-python-subproccess/23654936
class ForkablePdb(pdb.Pdb):

    _original_stdin_fd = sys.stdin.fileno()
    _original_stdin = None

    def __init__(self, stdout_fd=None, stderr_fd=None):
        pdb.Pdb.__init__(self, nosigint=True)
        self._stdout_fd = stdout_fd
        self._stderr_fd = stderr_fd

    def _cmdloop(self):
        current_stdin = sys.stdin
        try:
            if not self._original_stdin:
                self._original_stdin = os.fdopen(self._original_stdin_fd)
            sys.stdin = self._original_stdin
            if self._stdout_fd is not None:
                os.dup2(self._stdout_fd, sys.stdout.fileno())
                os.dup2(self._stdout_fd, self.stdout.fileno())
            if self._stderr_fd is not None:
                os.dup2(self._stderr_fd, sys.stderr.fileno())
            self.cmdloop()
        finally:
            sys.stdin = current_stdin
