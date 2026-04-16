# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import io
import sys
import warnings

import spack.llnl.util.tty as tty
from spack.util.log_parse import make_log_context, parse_log_events

description = "filter errors and warnings from build logs"
section = "developer"
level = "long"

event_types = ("errors", "warnings")


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "--show",
        action="store",
        default="errors",
        help="comma-separated list of what to show; options: errors, warnings",
    )
    subparser.add_argument(
        "-c",
        "--context",
        action="store",
        type=int,
        default=3,
        help="lines of context to show around lines of interest",
    )
    subparser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        help="print out a profile of time spent in regexes during parse",
    )
    subparser.add_argument(
        "-w", "--width", action="store", type=int, default=None, help=argparse.SUPPRESS
    )
    subparser.add_argument(
        "-j", "--jobs", action="store", type=int, default=None, help=argparse.SUPPRESS
    )

    subparser.add_argument("file", help="a log file containing build output, or - for stdin")


def log_parse(parser, args):
    input = args.file
    if args.file == "-":
        input = io.TextIOWrapper(
            sys.stdin.buffer, encoding="utf-8", errors="replace", closefd=False
        )

    if args.width is not None:
        warnings.warn("The --width option is deprecated and will be removed in Spack v1.3")
    if args.jobs is not None:
        warnings.warn("The --jobs option is deprecated and will be removed in Spack v1.3")

    log_errors, log_warnings = parse_log_events(input, args.context, args.profile)
    if args.profile:
        return

    types = [s.strip() for s in args.show.split(",")]
    for e in types:
        if e not in event_types:
            tty.die("Invalid event type: %s" % e)

    events = []
    if "errors" in types:
        events.extend(log_errors)
        print("%d errors" % len(log_errors))
    if "warnings" in types:
        events.extend(log_warnings)
        print("%d warnings" % len(log_warnings))

    print(make_log_context(events), end="")
