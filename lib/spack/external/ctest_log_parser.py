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

    https://github.com/Kitware/CMake/blob/master/Source/CTest/cmCTestBuildHandler.cxx

This file takes the regexes verbatim from there and adds some parsing
algorithms that duplicate the way CTest scrapes log files.  To keep this
up to date with CTest, just make sure the ``*_matches`` and
``*_exceptions`` lists are kept up to date with CTest's build handler.
"""
import re
from six import StringIO
from six import string_types


error_matches = [
    "^[Bb]us [Ee]rror",
    "^[Ss]egmentation [Vv]iolation",
    "^[Ss]egmentation [Ff]ault",
    ":.*[Pp]ermission [Dd]enied",
    "([^ :]+):([0-9]+): ([^ \\t])",
    "([^:]+): error[ \\t]*[0-9]+[ \\t]*:",
    "^Error ([0-9]+):",
    "^Fatal",
    "^Error: ",
    "^Error ",
    "[0-9] ERROR: ",
    "^\"[^\"]+\", line [0-9]+: [^Ww]",
    "^cc[^C]*CC: ERROR File = ([^,]+), Line = ([0-9]+)",
    "^ld([^:])*:([ \\t])*ERROR([^:])*:",
    "^ild:([ \\t])*\\(undefined symbol\\)",
    "([^ :]+) : (error|fatal error|catastrophic error)",
    "([^:]+): (Error:|error|undefined reference|multiply defined)",
    "([^:]+)\\(([^\\)]+)\\) ?: (error|fatal error|catastrophic error)",
    "^fatal error C[0-9]+:",
    ": syntax error ",
    "^collect2: ld returned 1 exit status",
    "ld terminated with signal",
    "Unsatisfied symbol",
    "^Unresolved:",
    "Undefined symbol",
    "^Undefined[ \\t]+first referenced",
    "^CMake Error.*:",
    ":[ \\t]cannot find",
    ":[ \\t]can't find",
    ": \\*\\*\\* No rule to make target [`'].*\\'.  Stop",
    ": \\*\\*\\* No targets specified and no makefile found",
    ": Invalid loader fixup for symbol",
    ": Invalid fixups exist",
    ": Can't find library for",
    ": internal link edit command failed",
    ": Unrecognized option [`'].*\\'",
    "\", line [0-9]+\\.[0-9]+: [0-9]+-[0-9]+ \\([^WI]\\)",
    "ld: 0706-006 Cannot find or open library file: -l ",
    "ild: \\(argument error\\) can't find library argument ::",
    "^could not be found and will not be loaded.",
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

error_exceptions = [
    "instantiated from ",
    "candidates are:",
    ": warning",
    ": \\(Warning\\)",
    ": note",
    "Note:",
    "makefile:",
    "Makefile:",
    ":[ \\t]+Where:",
    "([^ :]+):([0-9]+): Warning",
    "------ Build started: .* ------",
]

#: Regexes to match file/line numbers in error/warning messages
warning_matches = [
    "([^ :]+):([0-9]+): warning:",
    "([^ :]+):([0-9]+): note:",
    "^cc[^C]*CC: WARNING File = ([^,]+), Line = ([0-9]+)",
    "^ld([^:])*:([ \\t])*WARNING([^:])*:",
    "([^:]+): warning ([0-9]+):",
    "^\"[^\"]+\", line [0-9]+: [Ww](arning|arnung)",
    "([^:]+): warning[ \\t]*[0-9]+[ \\t]*:",
    "^(Warning|Warnung) ([0-9]+):",
    "^(Warning|Warnung)[ :]",
    "WARNING: ",
    "([^ :]+) : warning",
    "([^:]+): warning",
    "\", line [0-9]+\\.[0-9]+: [0-9]+-[0-9]+ \\([WI]\\)",
    "^cxx: Warning:",
    ".*file: .* has no symbols",
    "([^ :]+):([0-9]+): (Warning|Warnung)",
    "\\([0-9]*\\): remark #[0-9]*",
    "\".*\", line [0-9]+: remark\\([0-9]*\\):",
    "cc-[0-9]* CC: REMARK File = .*, Line = [0-9]*",
    "^CMake Warning.*:",
    "^\\[WARNING\\]",
]

#: Regexes to match file/line numbers in error/warning messages
warning_exceptions = [
    "/usr/.*/X11/Xlib\\.h:[0-9]+: war.*: ANSI C\\+\\+ forbids declaration",
    "/usr/.*/X11/Xutil\\.h:[0-9]+: war.*: ANSI C\\+\\+ forbids declaration",
    "/usr/.*/X11/XResource\\.h:[0-9]+: war.*: ANSI C\\+\\+ forbids declaration",
    "WARNING 84 :",
    "WARNING 47 :",
    "makefile:",
    "Makefile:",
    "warning:  Clock skew detected.  Your build may be incomplete.",
    "/usr/openwin/include/GL/[^:]+:",
    "bind_at_load",
    "XrmQGetResource",
    "IceFlush",
    "warning LNK4089: all references to [^ \\t]+ discarded by .OPT:REF",
    "ld32: WARNING 85: definition of dataKey in",
    "cc: warning 422: Unknown option \"\\+b",
    "_with_warning_C",
]

#: Regexes to match file/line numbers in error/warning messages
file_line_matches = [
    "^Warning W[0-9]+ ([a-zA-Z.\\:/0-9_+ ~-]+) ([0-9]+):",
    "^([a-zA-Z./0-9_+ ~-]+):([0-9]+):",
    "^([a-zA-Z.\\:/0-9_+ ~-]+)\\(([0-9]+)\\)",
    "^[0-9]+>([a-zA-Z.\\:/0-9_+ ~-]+)\\(([0-9]+)\\)",
    "^([a-zA-Z./0-9_+ ~-]+)\\(([0-9]+)\\)",
    "\"([a-zA-Z./0-9_+ ~-]+)\", line ([0-9]+)",
    "File = ([a-zA-Z./0-9_+ ~-]+), Line = ([0-9]+)",
]


class LogEvent(object):
    """Class representing interesting events (e.g., errors) in a build log."""
    def __init__(self, text, line_no,
                 source_file=None, source_line_no=None,
                 pre_context=None, post_context=None):
        self.text = text
        self.line_no = line_no
        self.source_file = source_file,
        self.source_line_no = source_line_no,
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
        out = StringIO()
        for i in range(self.start, self.end):
            if i == self.line_no:
                out.write('  >> %-6d%s' % (i, self[i]))
            else:
                out.write('     %-6d%s' % (i, self[i]))
        return out.getvalue()


class BuildError(LogEvent):
    """LogEvent subclass for build errors."""


class BuildWarning(LogEvent):
    """LogEvent subclass for build warnings."""


def _match(matches, exceptions, line):
    """True if line matches a regex in matches and none in exceptions."""
    return (any(m.search(line) for m in matches) and
            not any(e.search(line) for e in exceptions))


class CTestLogParser(object):
    """Log file parser that extracts errors and warnings."""
    def __init__(self):
        def compile(regex_array):
            return [re.compile(regex) for regex in regex_array]

        self.error_matches      = compile(error_matches)
        self.error_exceptions   = compile(error_exceptions)
        self.warning_matches    = compile(warning_matches)
        self.warning_exceptions = compile(warning_exceptions)
        self.file_line_matches  = compile(file_line_matches)

    def parse(self, stream, context=6):
        """Parse a log file by searching each line for errors and warnings.

        Args:
            stream (str or file-like): filename or stream to read from
            context (int): lines of context to extract around each log event

        Returns:
            (tuple): two lists containig ``BuildError`` and
                ``BuildWarning`` objects.
        """
        if isinstance(stream, string_types):
            with open(stream) as f:
                return self.parse(f)

        lines = [line for line in stream]

        errors = []
        warnings = []
        for i, line in enumerate(lines):
            # use CTest's regular expressions to scrape the log for events
            if _match(self.error_matches, self.error_exceptions, line):
                event = BuildError(line.strip(), i + 1)
                errors.append(event)
            elif _match(self.warning_matches, self.warning_exceptions, line):
                event = BuildWarning(line.strip(), i + 1)
                warnings.append(event)
            else:
                continue

            # get file/line number for each event, if possible
            for flm in self.file_line_matches:
                match = flm.search(line)
                if match:
                    event.source_file, source_line_no = match.groups()

            # add log context, as well
            event.pre_context = [
                l.rstrip() for l in lines[i - context:i]]
            event.post_context = [
                l.rstrip() for l in lines[i + 1:i + context + 1]]

        return errors, warnings
