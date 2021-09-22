# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import sys

import six

import llnl.util.tty.colify as colify

import spack.environment as ev
import spack.repo

description = "list package tags"
section = "basic"
level = "long"


def get_installed_packages():
    env = ev.active_environment()
    hashes = env.all_hashes() if env else None
    return [spec.name for spec in spack.store.db.query(hashes=hashes)]


def get_tag_packages(tags, installed, skip_empty):
    tag_pkgs = collections.defaultdict(lambda: list)
    spec_names = get_installed_packages() if installed else []
    for tag in tags:
        packages = [name for name in spack.repo.path.tag_index[tag] if \
            not installed or name in spec_names]
        if packages or not skip_empty:
            tag_pkgs[tag] = packages
    return tag_pkgs


def report_tags(category, tags):
    buffer = six.StringIO()
    isatty = sys.stdout.isatty()

    if isatty:
        buffer.write("{0} package tags:\n".format(category))

    if tags:
        colify.colify(tags, output=buffer, tty=isatty, indent=4)
    else:
        buffer.write("    None\n")
    print(buffer.getvalue())


def setup_parser(subparser):
    subparser.epilog = "Processes available tags when called without tags."
    subparser.add_argument(
        '-i', '--installed', action='store_true', default=False,
        help="limit tags to those of installed packages"
    )
    subparser.add_argument(
        '-s', '--show-packages', action='store_true', default=False,
        help="show packages for available tags when no tags are provided"
    )
    subparser.add_argument(
        'tag',
        nargs='*',
        help="find packages that provide this tag"
    )


def tags(parser, args):
    # unique list of available tags
    available_tags = sorted(spack.repo.path.tag_index.keys())
    if not available_tags:
        print("There are no known tagged packages")
        return

    # Only report relevant tags if none are to be shown
    if not args.tag and not args.show_packages:
        if not args.installed:
            report_tags("Available", available_tags)
        else:
            tag_pkgs = get_tag_packages(available_tags, True, True)
            #tags = list(tag_pkgs.keys()) if tag_pkgs else []
            tags = tag_pkgs.keys() if tag_pkgs else []
            report_tags("Installed", tags)
        return

    # Report packages associated with tags
    buffer = six.StringIO()
    isatty = sys.stdout.isatty()

    tags = args.tag if args.tag else available_tags
    tag_pkgs = get_tag_packages(tags, args.installed, False)
    missing = "No installed packages" if args.installed else "None"
    for tag in sorted(tag_pkgs):
        packages = tag_pkgs[tag]
        if packages or not args.installed:
            if isatty:
                buffer.write("{0}:\n".format(tag))

            if packages:
                colify.colify(packages, output=buffer, tty=isatty, indent=4)
            else:
                buffer.write("    {0}\n".format(missing))
            buffer.write("\n")
    print(buffer.getvalue())
