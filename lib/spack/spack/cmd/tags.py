# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import io
import sys
from typing import Dict, Iterable, List

import spack.environment
import spack.llnl.string
import spack.llnl.util.tty as tty
import spack.llnl.util.tty.colify as colify
import spack.repo

description = "show package tags and associated packages"
section = "basic"
level = "long"


def report_tags(category, tags):
    buffer = io.StringIO()
    isatty = sys.stdout.isatty()

    if isatty:
        num = len(tags)
        fmt = "{0} package tag".format(category)
        buffer.write("{0}:\n".format(spack.llnl.string.plural(num, fmt)))

    if tags:
        colify.colify(tags, output=buffer, tty=isatty, indent=4)
    else:
        buffer.write("    None\n")
    print(buffer.getvalue())


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.epilog = (
        "Tags from known packages will be used if no tags are provided on "
        "the command\nline. If tags are provided, packages with at least one "
        "will be reported.\n\nYou are not allowed to provide tags and use "
        "'--all' at the same time."
    )
    subparser.add_argument(
        "-i",
        "--installed",
        action="store_true",
        default=False,
        help="show information for installed packages only",
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        default=False,
        help="show packages for all available tags",
    )
    subparser.add_argument("tag", nargs="*", help="show packages with the specified tag")


def tags(parser, args):
    # Disallow combining all option with (positional) tags to avoid confusion
    if args.all and args.tag:
        tty.die("Use the '--all' option OR provide tag(s) on the command line")

    # Provide a nice, simple message if database is empty
    if args.installed and not spack.environment.installed_specs():
        tty.msg("No installed packages")
        return

    # unique list of available tags
    available_tags = sorted(spack.repo.PATH.tag_index.tags)
    if not available_tags:
        tty.msg("No tagged packages")
        return

    show_packages = args.tag or args.all

    # Only report relevant, available tags if no packages are to be shown
    if not show_packages:
        if not args.installed:
            report_tags("available", available_tags)
        else:
            tag_pkgs = packages_with_tags(available_tags, True, True)
            tags = tag_pkgs.keys() if tag_pkgs else []
            report_tags("installed", tags)
        return

    # Report packages associated with tags
    buffer = io.StringIO()
    isatty = sys.stdout.isatty()

    tags = args.tag if args.tag else available_tags
    tag_pkgs = packages_with_tags(tags, args.installed, False)
    missing = "No installed packages" if args.installed else "None"
    for tag in sorted(tag_pkgs):
        # TODO: Remove the sorting once we're sure noone has an old
        # TODO: tag cache since it can accumulate duplicates.
        packages = sorted(list(set(tag_pkgs[tag])))
        if isatty:
            buffer.write("{0}:\n".format(tag))

        if packages:
            colify.colify(packages, output=buffer, tty=isatty, indent=4)
        else:
            buffer.write("    {0}\n".format(missing))
        buffer.write("\n")
    print(buffer.getvalue())


def packages_with_tags(
    tags: Iterable[str], installed: bool, skip_empty: bool
) -> Dict[str, List[str]]:
    """
    Returns a dict, indexed by tag, containing lists of names of packages
    containing the tag or, if no tags, for all available tags.

    Arguments:
        tags: list of tags of interest or None for all
        installed: True if want names of packages that are installed;
            otherwise, False if want all packages with the tag
        skip_empty: True if exclude tags with no associated packages;
            otherwise, False if want entries for all tags even when no such
            tagged packages
    """
    tag_pkgs: Dict[str, List[str]] = {}
    name_filter = {x.name for x in spack.environment.installed_specs()} if installed else None
    for tag in tags:
        packages = spack.repo.PATH.tag_index.get_packages(tag)
        if name_filter is not None:
            packages = [p for p in packages if p in name_filter]
        if packages or not skip_empty:
            tag_pkgs[tag] = packages
    return tag_pkgs
