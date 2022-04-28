# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
        '--keep-stage', action='store_true', default=False,
        help="don't clean up staging area when command completes")
    sp = subparser.add_mutually_exclusive_group()
    sp.add_argument(
        '-b', '--batch', action='store_true', default=False,
        help="don't ask which versions to checksum")
    sp.add_argument(
        '-l', '--latest', action='store_true', default=False,
        help="checksum the latest available version only")
    sp.add_argument(
        '-p', '--preferred', action='store_true', default=False,
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
    versions = args.versions
    if (not versions) and args.preferred:
        versions = [preferred_version(pkg)]

    if versions:
        remote_versions = None
        for version in versions:
            version = ver(version)
            if not isinstance(version, Version):
                tty.die("Cannot generate checksums for version lists or "
                        "version ranges. Use unambiguous versions.")
            url = pkg.find_valid_url_for_version(version)
            if url is not None:
                url_dict[version] = url
                continue
            # if we get here, it's because no valid url was provided by the package
            # do expensive fallback to try to recover
            if remote_versions is None:
                remote_versions = pkg.fetch_remote_versions()
            if version in remote_versions:
                url_dict[version] = remote_versions[version]
    else:
        url_dict = pkg.fetch_remote_versions()

    if not url_dict:
        tty.die("Could not find any versions for {0}".format(pkg.name))

    version_lines = spack.stage.get_checksums_for_versions(
        url_dict, pkg.name, keep_stage=args.keep_stage,
        batch=(args.batch or len(args.versions) > 0 or len(url_dict) == 1),
        latest=args.latest, fetch_options=pkg.fetch_options)

    print()
    print(version_lines)
    print()
