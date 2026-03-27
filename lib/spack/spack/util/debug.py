# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Debug signal handler: enters pdb on ctrl-C."""
import os
import signal

_DEBUG_PID = None


def debug_handler(sig, frame):
    """Signal handler for SIGINT. Enters pdb if the signal is sent to this process."""
    if os.getpid() != _DEBUG_PID:
        raise KeyboardInterrupt

    import pdb

    pdb.Pdb().set_trace(frame)


def register_interrupt_handler():
    """Register the debug handler for SIGINT."""
    global _DEBUG_PID
    _DEBUG_PID = os.getpid()
    signal.signal(signal.SIGINT, debug_handler)
