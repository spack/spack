# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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

from collections import namedtuple
from contextlib import contextmanager
from collections import OrderedDict

Interval = namedtuple("Interval", ("start", "end"))


class Timer(object):
    """Simple interval timer"""

    def __init__(self, now=time.time):
        self.phases = OrderedDict()  # type: OrderedDict[str,Interval]
        self._now = now
        self._total = Interval(self._now(), end=None)

    def start(self, name=None):
        interval = Interval(self._now(), None)
        if name is None:
            self._total = interval
        else:
            self.phases[name] = interval

    def stop(self, name=None):
        if name is None:
            self._total = Interval(self._total.start, self._now())
        else:
            self.phases[name] = Interval(self.phases[name].start, self._now())

    def duration(self, name=None):
        interval = self._total if name is None else self.phases[name]
        end = self._now() if interval.end is None else interval.end
        return end - interval.start

    @contextmanager
    def phase(self, name):
        start = self._now()
        yield
        self.phases[name] = Interval(start, self._now())

    def write_json(self, out=sys.stdout):
        """
        Write a json object with times to file
        """
        phases = [{"name": p, "seconds": self.duration(p)} for p in self.phases.keys()]
        times = {"phases": phases, "total": {"seconds": self.duration()}}
        out.write(sjson.dump(times))

    def write_tty(self, out=sys.stdout):
        out.write("Time:\n")
        for p in self.phases.keys():
            out.write("    %-15s%.4f\n" % (p + ":", self.duration(p)))
        out.write("Total: %.4f\n" % self.duration())
