##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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

import argparse
import os.path
import sys

import llnl.util.tty as tty
import spack
import spack.cmd
from spack.util.log_parse import parse_log_events, make_log_context


description = "query or manipulate installation logs"
section = "build"
level = "short"

event_types = ('errors', 'warnings')


def setup_parser(subparser):

    def add_spec_or_file(parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--spec', '-s',
            help='spec identifying a unique software installation'
        )
        group.add_argument(
            '--file', '-f',
            help='a log file containing build output, or - for stdin'
        )

    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='log_command')

    # log show
    show_parser = sp.add_parser(
        'show', help='show the build logs of an installed spec')
    show_parser.add_argument(
        'spec',
        nargs=argparse.REMAINDER,
        help="spec identifying a unique software installation"
    )

    # log parse
    parse = sp.add_parser(
        'parse', help='filter errors and warnings from build logs')
    add_spec_or_file(parse)
    parse.add_argument(
        '--show', action='store', default='errors',
        help='comma-separated list of what to show; options: errors, warnings')
    parse.add_argument(
        '-c', '--context', action='store', type=int, default=3,
        help='lines of context to show around lines of interest')
    parse.add_argument(
        '-p', '--profile', action='store_true',
        help='print out a profile of time spent in regexes during parse')
    parse.add_argument(
        '-w', '--width', action='store', type=int, default=None,
        help='wrap width: auto-size to terminal by default; 0 for no wrap')
    parse.add_argument(
        '-j', '--jobs', action='store', type=int, default=None,
        help='number of jobs to parse log file (default: 1 for short logs, '
             'ncpus for long logs)')


def _build_log_for_spec(spec):
    """Get the absolute path of the build log associated with an
    installed spec.

    Dies in case of an error.

    Args:
        spec (str): spec to be parsed

    Returns:
        absolute path of the build logs
    """
    specs = spack.cmd.parse_specs(spec)

    if len(specs) != 1:
        msg = 'only one spec is allowed in the query [{0} given]'
        tty.die(msg.format(len(specs)))

    spec = spack.cmd.disambiguate_spec(specs[0])

    if spec.external:
        msg = '{0} is an external and has no logs.'
        tty.die(msg.format_map(spec.short_spec))

    filename = 'build.out'
    abs_filename = os.path.join(spec.prefix, '.spack', filename)
    if not os.path.exists(abs_filename):
        msg = 'log file does not exist! [{0}]'
        tty.die(msg.format(abs_filename))

    return abs_filename


def _get_abspath_of_build_log(args):
    abs_filename = args.file
    if args.spec is not None:
        abs_filename = _build_log_for_spec(args.spec)
    abs_filename = os.path.abspath(abs_filename)
    return abs_filename


def log_show(parser, args):
    abs_filename = _build_log_for_spec(args.spec)
    with open(abs_filename, 'r') as file_stream:
        print(''.join(file_stream.readlines()))


def log_parse(parser, args):
    input = sys.stdin if args.file == '-' else _get_abspath_of_build_log(args)
    errors, warnings = parse_log_events(
        input, args.context, args.jobs, args.profile)

    if args.profile:
        return

    types = [s.strip() for s in args.show.split(',')]
    for e in types:
        if e not in event_types:
            tty.die('Invalid event type: %s' % e)

    events = []
    if 'errors' in types:
        events.extend(errors)
        print('%d errors' % len(errors))
    if 'warnings' in types:
        events.extend(warnings)
        print('%d warnings' % len(warnings))

    print(make_log_context(events, args.width))


def log(parser, args):
    action = {
        'show': log_show,
        'parse': log_parse,
    }
    action[args.log_command](parser, args)
