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
from collections import OrderedDict, namedtuple
from contextlib import contextmanager

from llnl.util.lang import pretty_seconds

import spack.util.spack_json as sjson

Interval = namedtuple("Interval", ("begin", "end"))


class Timer(object):
    """Simple interval timer"""

    def __init__(self, now=time.time):
        self._now = now
        self._timers = OrderedDict()  # type: OrderedDict[str,Interval]
        self._timers["_global"] = Interval(self._now(), end=None)

    def start(self, name="_global"):
        self._timers[name] = Interval(self._now(), None)

    def stop(self, name="_global"):
        interval = self._timers.get(name, None)
        if not interval:
            return
        self._timers[name] = Interval(interval.begin, self._now())

    def duration(self, name="_global"):
        try:
            interval = self._timers[name]
        except KeyError:
            return 0.0
        end = self._now() if interval.end is None else interval.end
        return end - interval.begin

    @contextmanager
    def measure(self, name):
        begin = self._now()
        yield
        self._timers[name] = Interval(begin, self._now())

    @property
    def phases(self):
        return [k for k in self._timers.keys() if k != "_global"]

    def write_json(self, out=sys.stdout):
        """
        Write a json object with times to file
        """
        phases = [{"name": p, "seconds": self.duration(p)} for p in self.phases]
        times = {"phases": phases, "total": {"seconds": self.duration()}}
        out.write(sjson.dump(times))

    def write_tty(self, out=sys.stdout):
        for p in self.phases:
            out.write("    {:10s} {:>10s}\n".format(p, pretty_seconds(self.duration(p))))
        out.write("    {:10s} {:>10s}\n".format("total", pretty_seconds(self.duration())))
