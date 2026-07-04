# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.cmd.path as path
from spack.llnl.util.tty.color import colorize

description = "print package/dir locations (deprecated; use spack path)"
section = "query"
level = "long"

# `spack location` is deprecated in favor of `spack path`, and `spack location -i SPEC`
# is the same as `spack path SPEC`.

# This is a thin wrapper around `spack.cmd.path`, and can be removed if/when `spack location`
# is no longer needed.

_help = colorize(
    "@*Y{Warning:} @*{spack location} is deprecated; use @*{spack path} instead.\n\n"
    "@*{spack path} takes all the same options as @*{spack location}, but it prints the\n"
    "install prefix (-i) by default instead of the source directory (-c).\n"
)


def setup_parser(subparser):
    # `location` shares `path`'s options, but overrides the help text so that
    # `spack location -h` shows the deprecation warning above.
    path.setup_parser(subparser)
    subparser.description = _help


def requested_a_directory(args) -> bool:
    """Whether the user selected any of `path`'s directory options."""
    # find the group defined by `path.setup_parser`, which will have an `install_dir` attr
    groups = args.subparser._mutually_exclusive_groups
    group = next(g for g in groups if any(a.dest == "install_dir" for a in g._group_actions))

    # see if anything was specified explicitly by the user
    return any(getattr(args, a.dest) != a.default for a in group._group_actions)


def location(parser, args):
    # Unlike `spack path`, `location` defaults to a spec's source dir rather
    # than its install prefix. No runtime warning is emitted here on purpose.
    if not requested_a_directory(args):
        args.source_dir = True
    path.print_path(parser, args)
