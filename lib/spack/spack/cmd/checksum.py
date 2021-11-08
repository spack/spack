# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.repo
import spack.stage
import spack.util.crypto
from spack.package import preferred_version
from spack.util.naming import valid_fully_qualified_module_name
from spack.version import Version, ver

description = "checksum available versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="don't clean up staging area when command completes")
    sp = subparser.add_mutually_exclusive_group()
    sp.add_argument(
        '-b', '--batch', action='store_true',
        help="don't ask which versions to checksum")
    sp.add_argument(
        '-l', '--latest', action='store_true',
        help="checksum the latest available version only")
    sp.add_argument(
        '-p', '--preferred', action='store_true',
        help="checksum the preferred version only")
    arguments.add_common_arguments(subparser, ['package'])
    subparser.add_argument(
        'versions', nargs=argparse.REMAINDER,
        help='versions to generate checksums for')


def checksum(parser, args):
    # Did the user pass 'package@version' string?
    if len(args.versions) == 0 and '@' in args.package:
        args.versions = [args.package.split('@')[1]]
        args.package = args.package.split('@')[0]

    # Make sure the user provided a package and not a URL
    if not valid_fully_qualified_module_name(args.package):
        tty.die("`spack checksum` accepts package names, not URLs.")

    # Get the package we're going to generate checksums for
    pkg = spack.repo.get(args.package)

    url_dict = {}
    if args.versions:
        # If the user asked for specific versions, use those
        for version in args.versions:
            version = ver(version)
            if not isinstance(version, Version):
                tty.die("Cannot generate checksums for version lists or "
                        "version ranges. Use unambiguous versions.")
            url_dict[version] = pkg.url_for_version(version)
    elif args.preferred:
        version = preferred_version(pkg)
        url_dict = dict([(version, pkg.url_for_version(version))])
    else:
        # Otherwise, see what versions we can find online
        url_dict = pkg.fetch_remote_versions()
        if not url_dict:
            tty.die("Could not find any versions for {0}".format(pkg.name))

        # And ensure the specified version URLs take precedence, if available
        try:
            explicit_dict = {}
            for v in pkg.versions:
                if not v.isdevelop():
                    explicit_dict[v] = pkg.url_for_version(v)
            url_dict.update(explicit_dict)
        except spack.package.NoURLError:
            pass

    version_lines = spack.stage.get_checksums_for_versions(
        url_dict, pkg.name, keep_stage=args.keep_stage,
        batch=(args.batch or len(args.versions) > 0 or len(url_dict) == 1),
        latest=args.latest, fetch_options=pkg.fetch_options)

    print()
    print(version_lines)
    print()
