##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from __future__ import print_function

import re
from six import StringIO

from llnl.util.tty.color import colorize


class LogEvent(object):
    """Class representing interesting events (e.g., errors) in a build log."""
    def __init__(self, text, line_no,
                 pre_context='', post_context='', repeat_count=0):
        self.text = text
        self.line_no = line_no
        self.pre_context = pre_context
        self.post_context = post_context
        self.repeat_count = repeat_count

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


def parse_log_events(logfile, context=6):
    """Extract interesting events from a log file as a list of LogEvent.

    Args:
        logfile (str): name of the build log to parse
        context (int): lines of context to extract around each log event

    Currently looks for lines that contain the string 'error:', ignoring case.

    TODO: Extract warnings and other events from the build log.
    """
    with open(logfile, 'r') as f:
        lines = [line for line in f]

    log_events = []
    for i, line in enumerate(lines):
        if re.search('\berror:', line, re.IGNORECASE):
            event = LogEvent(
                line.strip(),
                i + 1,
                [l.rstrip() for l in lines[i - context:i]],
                [l.rstrip() for l in lines[i + 1:i + context + 1]])
            log_events.append(event)
    return log_events


def make_log_context(log_events):
    """Get error context from a log file.

    Args:
        log_events (list of LogEvent): list of events created by, e.g.,
            ``parse_log_events``

    Returns:
        str: context from the build log with errors highlighted

    Parses the log file for lines containing errors, and prints them out
    with line numbers and context.  Errors are highlighted with '>>' and
    with red highlighting (if color is enabled).
    """
    error_lines = set(e.line_no for e in log_events)

    out = StringIO()
    next_line = 1
    for event in log_events:
        start = event.start

        if start > next_line:
            out.write('     [ ... ]\n')

        if start < next_line:
            start = next_line

        for i in range(start, event.end):
            if i in error_lines:
                out.write(colorize('  @R{>> %-6d%s}\n' % (i, event[i])))
            else:
                out.write('     %-6d%s\n' % (i, event[i]))

        next_line = event.end

    return out.getvalue()
