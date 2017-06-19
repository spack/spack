##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

import argparse
import hashlib

import llnl.util.tty as tty
import spack
import spack.cmd
import spack.util.crypto
from spack.stage import Stage, FailedDownloadError
from spack.util.naming import *
from spack.version import *

description = "checksum available versions of a package"


def setup_parser(subparser):
    subparser.add_argument(
        'package',
        help='package to checksum versions for')
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="don't clean up staging area when command completes")
    subparser.add_argument(
        'versions', nargs=argparse.REMAINDER,
        help='versions to generate checksums for')


def get_checksums(url_dict, name, **kwargs):
    """Fetches and checksums archives from URLs.

    This function is called by both ``spack checksum`` and ``spack create``.
    The ``first_stage_function`` kwarg allows ``spack create`` to determine
    things like the build system of the archive.

    :param dict url_dict: A dictionary of the form: version -> URL
    :param str name: The name of the package
    :param callable first_stage_function: Function to run on first staging area
    :param bool keep_stage: Don't clean up staging area when command completes

    :returns: A multi-line string containing versions and corresponding hashes
    :rtype: str
    """
    first_stage_function = kwargs.get('first_stage_function', None)
    keep_stage = kwargs.get('keep_stage', False)

    sorted_versions = sorted(url_dict.keys(), reverse=True)

    # Find length of longest string in the list for padding
    max_len = max(len(str(v)) for v in sorted_versions)
    num_ver = len(sorted_versions)

    tty.msg("Found {0} version{1} of {2}:".format(
            num_ver, '' if num_ver == 1 else 's', name),
            "",
            *spack.cmd.elide_list(
                ["{0:{1}}  {2}".format(v, max_len, url_dict[v])
                 for v in sorted_versions]))
    print()

    archives_to_fetch = tty.get_number(
        "How many would you like to checksum?", default=1, abort='q')

    if not archives_to_fetch:
        tty.die("Aborted.")

    versions = sorted_versions[:archives_to_fetch]
    urls = [url_dict[v] for v in versions]

    tty.msg("Downloading...")
    version_hashes = []
    i = 0
    for url, version in zip(urls, versions):
        try:
            with Stage(url, keep=keep_stage) as stage:
                # Fetch the archive
                stage.fetch()
                if i == 0 and first_stage_function:
                    # Only run first_stage_function the first time,
                    # no need to run it every time
                    first_stage_function(stage, url)

                # Checksum the archive and add it to the list
                version_hashes.append((version, spack.util.crypto.checksum(
                    hashlib.md5, stage.archive_file)))
                i += 1
        except FailedDownloadError:
            tty.msg("Failed to fetch {0}".format(url))
        except Exception as e:
            tty.msg("Something failed on {0}, skipping.".format(url),
                    "  ({0})".format(e))

    if not version_hashes:
        tty.die("Could not fetch any versions for {0}".format(name))

    # Find length of longest string in the list for padding
    max_len = max(len(str(v)) for v, h in version_hashes)

    # Generate the version directives to put in a package.py
    version_lines = "\n".join([
        "    version('{0}', {1}'{2}')".format(
            v, ' ' * (max_len - len(str(v))), h) for v, h in version_hashes
    ])

    num_hash = len(version_hashes)
    tty.msg("Checksummed {0} version{1} of {2}".format(
        num_hash, '' if num_hash == 1 else 's', name))

    return version_lines


def checksum(parser, args):
    # Make sure the user provided a package and not a URL
    if not valid_fully_qualified_module_name(args.package):
        tty.die("`spack checksum` accepts package names, not URLs. "
                "Use `spack md5 <url>` instead.")

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

    version_lines = get_checksums(
        url_dict, pkg.name, keep_stage=args.keep_stage)

    print()
    print(version_lines)
