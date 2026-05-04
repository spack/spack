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
import re
import time
from collections import deque
from typing import Dict, Iterable, List, Optional, TextIO, Tuple, Union

from spack.llnl.util.lang import PatternStr

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

    #: color name when rendering in the terminal
    color = ""

    def __init__(
        self,
        text: str,
        line_no: int,
        source_file: Optional[str] = None,
        source_line_no: Optional[str] = None,
        pre_context: Optional[List[str]] = None,
        post_context: Optional[List[str]] = None,
    ) -> None:
        self.text = text
        self.line_no = line_no
        self.source_file = source_file
        self.source_line_no = source_line_no
        self.pre_context = pre_context if pre_context is not None else []
        self.post_context = post_context if post_context is not None else []
        self.repeat_count = 0

    @property
    def start(self) -> int:
        """First line in the log with text for the event or its context."""
        return self.line_no - len(self.pre_context)

    @property
    def end(self) -> int:
        """Last line in the log with text for event or its context."""
        return self.line_no + len(self.post_context) + 1

    def __getitem__(self, line_no: int) -> str:
        """Index event text and context by actual line number in file."""
        if line_no == self.line_no:
            return self.text
        elif line_no < self.line_no:
            return self.pre_context[line_no - self.line_no]
        else:
            return self.post_context[line_no - self.line_no - 1]

    def __str__(self) -> str:
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

    color = "R"


class BuildWarning(LogEvent):
    """LogEvent subclass for build warnings."""

    color = "Y"


def _optimize_regexes(regex_strings: List[str]) -> List[str]:
    """Groups regexes by their first character and combines each group into a single regex using
    alternation. Python's regex compiler optimizes the combined pattern to share common prefixes
    internally. The result is a shorter list of regexes that all hit a fast path in cpython's regex
    engine for prefix matching."""
    groups: Dict[str, List[str]] = {}
    for regex in sorted(regex_strings):
        key = regex[:1]  # empty or single character
        if key == "\\":  # include escaped character
            key = regex[:2]
        if key not in groups:
            groups[key] = [regex]
        else:
            groups[key].append(regex)
    return ["|".join(entries) for entries in groups.values()]


class _Matcher:
    """Tests a log line against match/exception regex lists."""

    def __init__(self, matches: List[PatternStr], exceptions: List[PatternStr]) -> None:
        self.matches = matches
        self.exceptions = exceptions

    def __call__(self, line: str) -> bool:
        """Returns True if line matches any regex in self.matches and none in self.exceptions."""
        for match in self.matches:
            if match.search(line):
                break
        else:
            return False
        for exc in self.exceptions:
            if exc.search(line):
                return False
        return True


class _ProfileMatcher(_Matcher):
    """Variant of _Matcher that records time spent in each regex."""

    def __init__(self, matches: List[PatternStr], exceptions: List[PatternStr]) -> None:
        super().__init__(matches, exceptions)
        self.match_times = [0.0] * len(matches)
        self.exc_times = [0.0] * len(exceptions)

    def __call__(self, line: str) -> bool:
        for i, m in enumerate(self.matches):
            start = time.perf_counter()
            found = m.search(line)
            self.match_times[i] += time.perf_counter() - start
            if found:
                break
        else:
            return False

        for i, m in enumerate(self.exceptions):
            start = time.perf_counter()
            found = m.search(line)
            self.exc_times[i] += time.perf_counter() - start
            if found:
                return False
        return True

    def print_timings(self, kind: str) -> None:
        print()
        print(f"{kind}_matches")
        for pattern, t in zip(self.matches, self.match_times):
            print("%16.2f        %s" % (t * 1e6, pattern.pattern))
        print()
        print(f"{kind}_exceptions")
        for pattern, t in zip(self.exceptions, self.exc_times):
            print("%16.2f        %s" % (t * 1e6, pattern.pattern))


def _parse(
    stream: Iterable[str],
    error_matcher: _Matcher,
    warning_matcher: _Matcher,
    file_line_matches: List[PatternStr],
    context: int,
    tail: int = 0,
) -> Tuple[List[BuildError], List[BuildWarning], Optional[LogEvent]]:

    errors: List[BuildError] = []
    warnings: List[BuildWarning] = []
    # rolling window of recent lines
    pre_context: deque[str] = deque(maxlen=max(context, tail))
    # list of (event, remaining_post_context_lines)
    pending_events: List[Tuple[Union[BuildError, BuildWarning], int]] = []

    last_line_no = 0
    for i, line in enumerate(stream):
        rstripped_line = line.rstrip()
        last_line_no = i + 1

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
        if error_matcher(line):
            event = BuildError(rstripped_line, i + 1)
        elif warning_matcher(line):
            event = BuildWarning(rstripped_line, i + 1)
        else:
            pre_context.append(rstripped_line)
            continue

        event.pre_context = list(pre_context)[-context:] if context else []
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

    # build tail section from the last N lines of the log, if requested
    if tail > 0 and last_line_no > 0:
        lines = list(pre_context)[-tail:]
        tail_event = LogEvent(text=lines[-1], line_no=last_line_no, pre_context=lines[:-1])
    else:
        tail_event = None

    return errors, warnings, tail_event


class CTestLogParser:
    """Log file parser that extracts errors and warnings."""

    def __init__(self, profile: bool = False) -> None:
        error_matches = [re.compile(r) for r in _optimize_regexes(_error_matches)]
        error_exceptions = [re.compile(r) for r in _optimize_regexes(_error_exceptions)]
        warning_matches = [re.compile(r) for r in _optimize_regexes(_warning_matches)]
        warning_exceptions = [re.compile(r) for r in _optimize_regexes(_warning_exceptions)]

        cls = _ProfileMatcher if profile else _Matcher
        self._error_matcher = cls(error_matches, error_exceptions)
        self._warning_matcher = cls(warning_matches, warning_exceptions)
        self._file_line_matches = [re.compile(r) for r in _file_line_matches]

    def print_timings(self) -> None:
        """Print out profile of time spent in different regular expressions."""
        assert isinstance(self._error_matcher, _ProfileMatcher)
        assert isinstance(self._warning_matcher, _ProfileMatcher)
        self._error_matcher.print_timings("error")
        self._warning_matcher.print_timings("warning")

    def parse(
        self, stream: Union[str, TextIO, List[str]], context: int = 6, tail: int = 0
    ) -> Tuple[List[BuildError], List[BuildWarning], Optional[LogEvent]]:
        """Parse a log file by searching each line for errors and warnings.

        Args:
            stream: filename or stream to read from
            context: lines of context to extract around each log event
            tail: if > 0, also return a :class:`LogEvent` with the last ``tail`` lines

        Returns:
            two lists containing :class:`BuildError` and :class:`BuildWarning` objects,
            plus an optional :class:`LogEvent` for the tail (None when ``tail=0``).
        """
        if isinstance(stream, str):
            with open(stream, encoding="utf-8", errors="replace") as f:
                return self.parse(f, context, tail)

        return _parse(
            stream,
            self._error_matcher,
            self._warning_matcher,
            self._file_line_matches,
            context,
            tail,
        )
