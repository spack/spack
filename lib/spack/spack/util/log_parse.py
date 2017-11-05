##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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

from six import StringIO

from ctest_log_parser import CTestLogParser
from llnl.util.tty.color import colorize


def parse_log_events(stream, context=6):
    """Extract interesting events from a log file as a list of LogEvent.

    Args:
        stream (str or fileobject): build log name or file object
        context (int): lines of context to extract around each log event

    Returns:
        (tuple): two lists containig ``BuildError`` and
            ``BuildWarning`` objects.

    This is a wrapper around ``ctest_log_parser.CTestLogParser`` that
    lazily constructs a single ``CTestLogParser`` object.  This ensures
    that all the regex compilation is only done once.
    """
    if parse_log_events.ctest_parser is None:
        parse_log_events.ctest_parser = CTestLogParser()

    return parse_log_events.ctest_parser.parse(stream, context)


#: lazily constructed CTest log parser
parse_log_events.ctest_parser = None


def make_log_context(log_events):
    """Get error context from a log file.

    Args:
        log_events (list of LogEvent): list of events created by
            ``ctest_log_parser.parse()``

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
