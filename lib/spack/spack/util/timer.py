# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Debug signal handler: prints a stack trace and enters interpreter.

``register_interrupt_handler()`` enables a ctrl-C handler that prints
a stack trace and drops the user into an interpreter.

"""
import sys
import time

import spack.util.spack_json as sjson


class Timer(object):
    """
    Simple timer for timing phases of a solve or install
    """
    def __init__(self):
        self.start = time.time()
        self.last = self.start
        self.phases = {}
        self.end = None

    def phase(self, name):
        last = self.last
        now = time.time()
        self.phases[name] = now - last
        self.last = now

    @property
    def total(self):
        """Return the total time
        """
        if self.end:
            return self.end - self.start
        return time.time() - self.start

    def stop(self):
        """
        Stop the timer to record a total time, if desired.
        """
        self.end = time.time()

    def write_json(self, out=sys.stdout):
        """
        Write a json object with times to file
        """
        phases = [{"name": p, "seconds": s} for p, s in self.phases.items()]
        times = {"phases": phases, "total": {"seconds": self.total}}
        out.write(sjson.dump(times))

    def write_tty(self, out=sys.stdout):
        now = time.time()
        out.write("Time:\n")
        for phase, t in self.phases.items():
            out.write("    %-15s%.4f\n" % (phase + ":", t))
        out.write("Total: %.4f\n" % (now - self.start))
