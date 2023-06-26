# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Debug signal handler: prints a stack trace and enters interpreter.

``register_interrupt_handler()`` enables a ctrl-C handler that prints
a stack trace and drops the user into an interpreter.

"""
import collections
import sys
import time
from contextlib import contextmanager
from typing import Dict

from llnl.util.lang import pretty_seconds_formatter

import spack.util.spack_json as sjson

Interval = collections.namedtuple("Interval", ("begin", "end"))


class BaseTimer:
    def start(self, name=None):
        pass

    def stop(self, name=None):
        pass

    def duration(self, name=None):
        return 0.0

    @contextmanager
    def measure(self, name):
        yield NullTimer()

    def subtimer(self, name):
        return NullTimer()

    @property
    def phases(self):
        return []

    def write_json(self, out=sys.stdout):
        pass

    def write_tty(self, out=sys.stdout):
        pass


class NullTimer(BaseTimer):
    """Timer interface that does nothing, useful in for "tell
    don't ask" style code when timers are optional."""

    pass


class Timer(BaseTimer):
    """Simple interval timer"""

    def __init__(self, now=time.time):
        """
        Arguments:
            now: function that gives the seconds since e.g. epoch
        """
        self._now = now
        self._timers: Dict[str, Timer] = collections.OrderedDict()
        self._interval: Interval

        self._interval = Interval(self._now(), None)

    def start(self, name=None):
        """
        Start or restart a named timer, or the global timer when no name is given.

        Arguments:
            name (str): Optional name of the timer. When no name is passed, the
                global timer is started.
        """

        if name:
            if self._interval.end:
                self.start()
            self._timers[name] = Timer(self._now)
        else:
            # Reset all of the sub-timers when restarting the global timer
            self._timers = {}
            self._interval = Interval(self._now(), None)

    def stop(self, name=None, when=None):
        """
        Stop a named timer, or all timers when no name is given. Stopping a
        timer that has not started has no effect.

        Arguments:
            name (str): Optional name of the timer. When no name is passed, all
                timers are stopped.
        """
        if name in self._timers:
            self._timers[name].stop(when=when)
        else:
            if self._interval.end:
                return
            self._interval = Interval(self._interval.begin, when or self._now())
            for name in self._timers:
                self._timers[name].stop(when=self._interval.end)

    def duration(self, name=None):
        """
        Get the time in seconds of a named timer, or the total time if no
        name is passed. The duration is always 0 for timers that have not been
        started, no error is raised.

        Arguments:
            name (str): (Optional) name of the timer

        Returns:
            float: duration of timer.
        """
        try:
            if name:
                interval = self._timers[name]._interval
            else:
                interval = self._interval
        except KeyError:
            return 0.0
        # Take either the interval end, the global timer, or now.
        end = interval.end or self._interval.end or self._now()
        return end - interval.begin

    @contextmanager
    def measure(self, name):
        """
        Context manager that allows you to time a block of code.

        Arguments:
            name (str): Name of the timer
        """
        timer = Timer(self._now)
        self._timers[name] = timer
        yield timer
        timer.stop()

    def subtimer(self, name):
        """
        Get the Timer object for the named subtimer

        Arguments:
            name (str): Name of the timer
        """
        if name not in self._timers:
            self._timers[name] = Timer(self._now)
        return self._timers[name]

    @property
    def phases(self):
        """Get all named timers (excluding the global/total timer)"""
        return [k for k in self._timers.keys()]

    def flatten(self, depth=-1, extra_attributes={}):
        flat = {}
        if self._timers and not depth == 0:
            flat = {"seconds": self.duration(), "phases": []}
            phases = flat["phases"]
            for name, t in self._timers.items():
                phase = {"name": name}
                phase.update(t.flatten(depth=depth - 1))
                phases.append(phase)
        else:
            flat = {"seconds": self.duration()}

        if extra_attributes:
            flat.update(extra_attributes)
        return flat

    def write_json(self, out=sys.stdout, depth=-1, extra_attributes={}):
        """Write a json object with times to file"""
        out.write(sjson.dump(self.flatten(depth, extra_attributes)))

    def write_tty(self, out=sys.stdout):
        """Write a human-readable summary of timings (depth is 1)"""

        times = [self.duration(p) for p in self.phases]

        # Get a consistent unit for the time
        pretty_seconds = pretty_seconds_formatter(max(times))

        # Tuples of (phase, time) including total.
        formatted = list(zip(self.phases, times))
        formatted.append(("total", self.duration()))

        # Write to out
        for name, duration in formatted:
            out.write(f"    {name:10s} {pretty_seconds(duration):>10s}\n")


#: instance of a do-nothing timer
NULL_TIMER = NullTimer()
