# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
from spack.util.naming import valid_fully_qualified_module_name
from spack.version import ver, Version

description = "checksum available versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="don't clean up staging area when command completes")
    arguments.add_common_arguments(subparser, ['package'])
    subparser.add_argument(
        'versions', nargs=argparse.REMAINDER,
        help='versions to generate checksums for')


def checksum(parser, args):
    # Make sure the user provided a package and not a URL
    if not valid_fully_qualified_module_name(args.package):
        tty.die("`spack checksum` accepts package names, not URLs.")

    # Get the package we're going to generate checksums for
    pkg = spack.repo.get(args.package)

    if args.versions:
        # If the user asked for specific versions, use those
        url_dict = {}
        for version in args.versions:
            version = ver(version)
            if not isinstance(version, Version):
                tty.die("Cannot generate checksums for version lists or "
                        "version ranges. Use unambiguous versions.")
            url_dict[version] = pkg.url_for_version(version)
    else:
        # Otherwise, see what versions we can find online
        url_dict = pkg.fetch_remote_versions()
        if not url_dict:
            tty.die("Could not find any versions for {0}".format(pkg.name))

    version_lines = spack.stage.get_checksums_for_versions(
        url_dict, pkg.name, keep_stage=args.keep_stage,
        fetch_options=pkg.fetch_options)

    print()
    print(version_lines)
    print()
