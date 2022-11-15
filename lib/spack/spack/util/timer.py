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

#: name for the global timer (used in start(), stop(), duration() without arguments)
global_timer_name = "_global"


class NullTimer(object):
    """Timer interface that does nothing, useful in for "tell
    don't ask" style code when timers are optional."""

    def start(self, name=global_timer_name):
        pass

    def stop(self, name=global_timer_name):
        pass

    def duration(self, name=global_timer_name):
        return 0.0

    @contextmanager
    def measure(self, name):
        yield

    @property
    def phases(self):
        return []

    def write_json(self, out=sys.stdout):
        pass

    def write_tty(self, out=sys.stdout):
        pass


#: instance of a do-nothing timer
NULL_TIMER = NullTimer()


class Timer(object):
    """Simple interval timer"""

    def __init__(self, now=time.time):
        """
        Arguments:
            now: function that gives the seconds since e.g. epoch
        """
        self._now = now
        self._timers = OrderedDict()  # type: OrderedDict[str,Interval]

        # _global is the overal timer since the instance was created
        self._timers[global_timer_name] = Interval(self._now(), end=None)

    def start(self, name=global_timer_name):
        """
        Start or restart a named timer, or the global timer when no name is given.

        Arguments:
            name (str): Optional name of the timer. When no name is passed, the
                global timer is started.
        """
        self._timers[name] = Interval(self._now(), None)

    def stop(self, name=global_timer_name):
        """
        Stop a named timer, or all timers when no name is given. Stopping a
        timer that has not started has no effect.

        Arguments:
            name (str): Optional name of the timer. When no name is passed, all
                timers are stopped.
        """
        interval = self._timers.get(name, None)
        if not interval:
            return
        self._timers[name] = Interval(interval.begin, self._now())

    def duration(self, name=global_timer_name):
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
            interval = self._timers[name]
        except KeyError:
            return 0.0
        # Take either the interval end, the global timer, or now.
        end = interval.end or self._timers[global_timer_name].end or self._now()
        return end - interval.begin

    @contextmanager
    def measure(self, name):
        """
        Context manager that allows you to time a block of code.

        Arguments:
            name (str): Name of the timer
        """
        begin = self._now()
        yield
        self._timers[name] = Interval(begin, self._now())

    @property
    def phases(self):
        """Get all named timers (excluding the global/total timer)"""
        return [k for k in self._timers.keys() if k != global_timer_name]

    def write_json(self, out=sys.stdout):
        """Write a json object with times to file"""
        phases = [{"name": p, "seconds": self.duration(p)} for p in self.phases]
        times = {"phases": phases, "total": {"seconds": self.duration()}}
        out.write(sjson.dump(times))

    def write_tty(self, out=sys.stdout):
        """Write a human-readable summary of timings"""
        # Individual timers ordered by registration
        formatted = [(p, pretty_seconds(self.duration(p))) for p in self.phases]

        # Total time
        formatted.append(("total", pretty_seconds(self.duration())))

        # Write to out
        for name, duration in formatted:
            out.write("    {:10s} {:>10s}\n".format(name, duration))
