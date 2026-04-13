# pylint: skip-file
# -----------------------------------------------------------------------------
# CMake - Cross Platform Makefile Generator
# Copyright 2000-2017 Kitware, Inc. and Contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# * Neither the name of Kitware, Inc. nor the names of Contributors
#   may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# -----------------------------------------------------------------------------
#
# The above copyright and license notice applies to distributions of
# CMake in source and binary form.  Third-party software packages supplied
# with CMake under compatible licenses provide their own copyright notices
# documented in corresponding subdirectories or source files.
#
# -----------------------------------------------------------------------------
#
# CMake was initially developed by Kitware with the following sponsorship:
#
#  * National Library of Medicine at the National Institutes of Health
#    as part of the Insight Segmentation and Registration Toolkit (ITK).
#
#  * US National Labs (Los Alamos, Livermore, Sandia) ASC Parallel
#    Visualization Initiative.
#
#  * National Alliance for Medical Image Computing (NAMIC) is funded by the
#    National Institutes of Health through the NIH Roadmap for Medical
#    Research, Grant U54 EB005149.
#
#  * Kitware, Inc.
# -----------------------------------------------------------------------------
"""Functions to parse build logs and extract error messages.

This is a python port of the regular expressions CTest uses to parse log
files here:

.. code-block::

   https://github.com/Kitware/CMake/blob/master/Source/CTest/cmCTestBuildHandler.cxx

This file takes the regexes verbatim from there and adds some parsing
algorithms that duplicate the way CTest scrapes log files.  To keep this
up to date with CTest, just make sure the ``*_matches`` and
``*_exceptions`` lists are kept up to date with CTest's build handler.
"""
import io
import math
import re
import time
from collections import deque
from contextlib import contextmanager
from typing import List, TextIO, Tuple, Union

_error_matches = [
    "^FAIL: ",
    "^FATAL: ",
    "^failed ",
    "FAILED",
    "Failed test",
    "^[Bb]us [Ee]rror",
    "^[Ss]egmentation [Vv]iolation",
    "^[Ss]egmentation [Ff]ault",
    "Permission [Dd]enied",
    "permission [Dd]enied",
    ":[0-9]+: [^ \\t]",
    ": error[ \\t]*[0-9]+[ \\t]*:",
    "^Error ([0-9]+):",
    "^Fatal",
    "^[Ee]rror: ",
    "^Error ",
    " ERROR: ",
    '^"[^"]+", line [0-9]+: [^Ww]',
    "^cc[^C]*CC: ERROR File = ([^,]+), Line = ([0-9]+)",
    "^ld([^:])*:([ \\t])*ERROR([^:])*:",
    "^ild:([ \\t])*\\(undefined symbol\\)",
    ": (error|fatal error|catastrophic error)",
    ": (Error:|error|undefined reference|multiply defined)",
    "\\([^\\)]+\\) ?: (error|fatal error|catastrophic error)",
    "^fatal error C[0-9]+:",
    ": syntax error ",
    "^collect2: ld returned 1 exit status",
    "ld terminated with signal",
    "Unsatisfied symbol",
    "^Unresolved:",
    "Undefined symbol",
    "^Undefined[ \\t]+first referenced",
    "^CMake Error",
    ":[ \\t]cannot find",
    ":[ \\t]can't find",
    ": \\*\\*\\* No rule to make target [`'].*\\'.  Stop",
    ": \\*\\*\\* No targets specified and no makefile found",
    ": Invalid loader fixup for symbol",
    ": Invalid fixups exist",
    ": Can't find library for",
    ": internal link edit command failed",
    ": Unrecognized option [`'].*\\'",
    '", line [0-9]+\\.[0-9]+: [0-9]+-[0-9]+ \\([^WI]\\)',
    "ld: 0706-006 Cannot find or open library file: -l ",
    "ild: \\(argument error\\) can't find library argument ::",
    "^could not be found and will not be loaded.",
    "^WARNING: '.*' is missing on your system",
    "s:616 string too big",
    "make: Fatal error: ",
    "ld: 0711-993 Error occurred while writing to the output file:",
    "ld: fatal: ",
    "final link failed:",
    "make: \\*\\*\\*.*Error",
    "make\\[.*\\]: \\*\\*\\*.*Error",
    "\\*\\*\\* Error code",
    "nternal error:",
    "Makefile:[0-9]+: \\*\\*\\* .*  Stop\\.",
    ": No such file or directory",
    ": Invalid argument",
    "^The project cannot be built\\.",
    "^\\[ERROR\\]",
    "^Command .* failed with exit code",
]

_error_exceptions = [
    "instantiated from ",
    "candidates are:",
    ": warning",
    ": WARNING",
    ": \\(Warning\\)",
    ": note",
    "    ok",
    "Note:",
    ":[ \\t]+Where:",
    ":[0-9]+: Warning",
    "------ Build started: .* ------",
]

#: Regexes to match file/line numbers in error/warning messages
_warning_matches = [
    ":[0-9]+: warning:",
    ":[0-9]+: note:",
    "^cc[^C]*CC: WARNING File = ([^,]+), Line = ([0-9]+)",
    "^ld([^:])*:([ \\t])*WARNING([^:])*:",
    ": warning [0-9]+:",
    '^"[^"]+", line [0-9]+: [Ww](arning|arnung)',
    ": warning[ \\t]*[0-9]+[ \\t]*:",
    "^(Warning|Warnung) ([0-9]+):",
    "^(Warning|Warnung)[ :]",
    "WARNING: ",
    ": warning",
    '", line [0-9]+\\.[0-9]+: [0-9]+-[0-9]+ \\([WI]\\)',
    "^cxx: Warning:",
    "file: .* has no symbols",
    ":[0-9]+: (Warning|Warnung)",
    "\\([0-9]*\\): remark #[0-9]*",
    '".*", line [0-9]+: remark\\([0-9]*\\):',
    "cc-[0-9]* CC: REMARK File = .*, Line = [0-9]*",
    "^CMake Warning",
    "^\\[WARNING\\]",
]

#: Regexes to match file/line numbers in error/warning messages
_warning_exceptions = [
    "/usr/.*/X11/Xlib\\.h:[0-9]+: war.*: ANSI C\\+\\+ forbids declaration",
    "/usr/.*/X11/Xutil\\.h:[0-9]+: war.*: ANSI C\\+\\+ forbids declaration",
    "/usr/.*/X11/XResource\\.h:[0-9]+: war.*: ANSI C\\+\\+ forbids declaration",
    "WARNING 84 :",
    "WARNING 47 :",
    "warning:  Clock skew detected.  Your build may be incomplete.",
    "/usr/openwin/include/GL/[^:]+:",
    "bind_at_load",
    "XrmQGetResource",
    "IceFlush",
    "warning LNK4089: all references to [^ \\t]+ discarded by .OPT:REF",
    "ld32: WARNING 85: definition of dataKey in",
    'cc: warning 422: Unknown option "\\+b',
    "_with_warning_C",
]

#: Regexes to match file/line numbers in error/warning messages
_file_line_matches = [
    "^Warning W[0-9]+ ([a-zA-Z.\\:/0-9_+ ~-]+) ([0-9]+):",
    "^([a-zA-Z./0-9_+ ~-]+):([0-9]+):",
    "^([a-zA-Z.\\:/0-9_+ ~-]+)\\(([0-9]+)\\)",
    "^[0-9]+>([a-zA-Z.\\:/0-9_+ ~-]+)\\(([0-9]+)\\)",
    "^([a-zA-Z./0-9_+ ~-]+)\\(([0-9]+)\\)",
    '"([a-zA-Z./0-9_+ ~-]+)", line ([0-9]+)',
    "File = ([a-zA-Z./0-9_+ ~-]+), Line = ([0-9]+)",
]


class LogEvent:
    """Class representing interesting events (e.g., errors) in a build log."""

    def __init__(
        self,
        text,
        line_no,
        source_file=None,
        source_line_no=None,
        pre_context=None,
        post_context=None,
    ):
        self.text = text
        self.line_no = line_no
        self.source_file = (source_file,)
        self.source_line_no = (source_line_no,)
        self.pre_context = pre_context if pre_context is not None else []
        self.post_context = post_context if post_context is not None else []
        self.repeat_count = 0

    @property
    def start(self):
        """First line in the log with text for the event or its context."""
        return self.line_no - len(self.pre_context)

    @property
    def end(self):
        """Last line in the log with text for event or its context."""
        return self.line_no + len(self.post_context) + 1

    def __getitem__(self, line_no):
        """Index event text and context by actual line number in file."""
        if line_no == self.line_no:
            return self.text
        elif line_no < self.line_no:
            return self.pre_context[line_no - self.line_no]
        elif line_no > self.line_no:
            return self.post_context[line_no - self.line_no - 1]

    def __str__(self):
        """Returns event lines and context."""
        out = io.StringIO()
        for i in range(self.start, self.end):
            if i == self.line_no:
                out.write("  >> %-6d%s" % (i, self[i]))
            else:
                out.write("     %-6d%s" % (i, self[i]))
        return out.getvalue()


class BuildError(LogEvent):
    """LogEvent subclass for build errors."""


class BuildWarning(LogEvent):
    """LogEvent subclass for build warnings."""


def chunks(xs, n):
    """Divide xs into n approximately-even chunks."""
    chunksize = int(math.ceil(len(xs) / n))
    return [xs[i : i + chunksize] for i in range(0, len(xs), chunksize)]


@contextmanager
def _time(times, i):
    start = time.time()
    yield
    end = time.time()
    times[i] += end - start


def _match(matches, exceptions, line):
    """True if line matches a regex in matches and none in exceptions."""
    return any(m.search(line) for m in matches) and not any(e.search(line) for e in exceptions)


def _profile_match(matches, exceptions, line, match_times, exc_times):
    """Profiled version of match().

    Timing is expensive so we have two whole functions.  This is much
    longer because we have to break up the ``any()`` calls.

    """
    for i, m in enumerate(matches):
        with _time(match_times, i):
            if m.search(line):
                break
    else:
        return False

    for i, m in enumerate(exceptions):
        with _time(exc_times, i):
            if m.search(line):
                return False
    else:
        return True


def _parse(stream, profile, context):
    def compile(regex_array):
        return [re.compile(regex) for regex in regex_array]

    error_matches = compile(_error_matches)
    error_exceptions = compile(_error_exceptions)
    warning_matches = compile(_warning_matches)
    warning_exceptions = compile(_warning_exceptions)
    file_line_matches = compile(_file_line_matches)

    matcher, _ = _match, []
    timings = []
    if profile:
        matcher = _profile_match
        timings = [
            [0.0] * len(error_matches),
            [0.0] * len(error_exceptions),
            [0.0] * len(warning_matches),
            [0.0] * len(warning_exceptions),
        ]

    errors = []
    warnings = []
    # rolling window of recent lines
    pre_context = deque(maxlen=context)
    # list of (event, remaining_post_context_lines)
    pending_events: List[Tuple[LogEvent, int]] = []

    for i, line in enumerate(stream):
        rstripped_line = line.rstrip()

        # feed this line into every event still collecting post_context
        if pending_events:
            active_events = []
            for event, remaining in pending_events:
                event.post_context.append(rstripped_line)
                if remaining > 1:
                    active_events.append((event, remaining - 1))
                elif isinstance(event, BuildError):
                    errors.append(event)
                else:
                    warnings.append(event)
            pending_events = active_events

        # use CTest's regular expressions to scrape the log for events
        if matcher(error_matches, error_exceptions, line, *timings[:2]):
            event = BuildError(rstripped_line, i + 1)
        elif matcher(warning_matches, warning_exceptions, line, *timings[2:]):
            event = BuildWarning(rstripped_line, i + 1)
        else:
            pre_context.append(rstripped_line)
            continue

        event.pre_context = list(pre_context)
        event.post_context = []

        # get file/line number for the event, if possible
        for flm in file_line_matches:
            match = flm.search(line)
            if match:
                event.source_file, event.source_line_no = match.groups()
                break

        if context > 0:
            pending_events.append((event, context))
        elif isinstance(event, BuildError):
            errors.append(event)
        else:
            warnings.append(event)

        pre_context.append(rstripped_line)

    # flush events whose post_context window extends past EOF
    for event, _ in pending_events:
        if isinstance(event, BuildError):
            errors.append(event)
        else:
            warnings.append(event)

    return errors, warnings, timings


class CTestLogParser:
    """Log file parser that extracts errors and warnings."""

    def __init__(self, profile=False):
        # whether to record timing information
        self.timings = []
        self.profile = profile

    def print_timings(self):
        """Print out profile of time spent in different regular expressions."""

        def stringify(elt):
            return elt if isinstance(elt, str) else elt.pattern

        index = 0
        for name, arr in [
            ("error_matches", _error_matches),
            ("error_exceptions", _error_exceptions),
            ("warning_matches", _warning_matches),
            ("warning_exceptions", _warning_exceptions),
        ]:

            print()
            print(name)
            for i, elt in enumerate(arr):
                print("%16.2f        %s" % (self.timings[index][i] * 1e6, stringify(elt)))
            index += 1

    def parse(
        self, stream: Union[str, TextIO], context: int = 6
    ) -> Tuple[List[BuildError], List[BuildWarning]]:
        """Parse a log file by searching each line for errors and warnings.

        Args:
            stream: filename or stream to read from
            context: lines of context to extract around each log event

        Returns:
            two lists containing :class:`BuildError` and :class:`BuildWarning` objects.
        """
        if isinstance(stream, str):
            with open(stream, encoding="utf-8", errors="replace") as f:
                return self.parse(f, context)

        errors, warnings, self.timings = _parse(stream, self.profile, context)
        return errors, warnings
