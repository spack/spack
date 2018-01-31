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
""" Stack spack installations - avoiding double-builds

Stack this spack repository on top of an external read-only spack installation
that already has several packages pre-built.

The installed packages in the remote spack-installation are symlinked into the
directory_layout of the current repository. Hardlinks make little to no sense
since the original files need to remain in place because dependencies are found
via RPATH (which are the old paths in the remote repository).
"""

from __future__ import print_function

__author__ = "Oliver Breitwieser (UHEI)"

import os
import os.path as osp
import spack
import spack.config
import spack.directory_layout
import spack.store
from spack.filesystem_view import filter_exclude
from spack.util.path import canonicalize_path
import llnl.util.tty as tty
import llnl.util.filesystem as fs

description = "integrate packages of remote spack repositories into this one"
section = "admin"
level = "long"  # TODO: re-check what 'level' is supposed to mean


def setup_parser(subparser):
    setup_parser.parser = subparser

    subparser.add_argument(
        '-e', '--exclude', action='append', default=[],
        help="exclude packages with names matching the given regex pattern")

    subparser.add_argument(
        '-n', '--no-stack-if-exists',
        action='store_true', default=False, dest="nostack",
        help="do not stack packages that are already stacked; the default is "
             "to overwrite all stacked packages with versions from the remote "
             "repository")

    subparser.add_argument(
        '--hardlinks',
        action='store_true', default=False,
        help="use hardlinks to stack repositories. This is NOT recommended as "
             "hard links cannot be differentiated from regular files. This "
             "means that unstacking external repositories has to be done "
             "manually and is very tedious... Be aware!")

    subparser.add_argument(
        "remotes", nargs="+",
        metavar='remote', action='store',
        help="one or more remote spack repositories which "
             "contain packages to be added as external packages")


def add_remote_packages(remote, exclude=[], nostack=False, hardlinks=False):
    """
        Add all installed packages in `remote` to the packages dictionary.

        If nostack == True, packages will not be re-linked if they exist.

        If hardlinks == True, packages will be hard-linked. Not recommended!
    """
    config = spack.config.get_config("config")

    # try to be intelligent and support both paths with and without
    # ./opt/spack-suffix
    remote_path = canonicalize_path(osp.join(remote, 'opt', 'spack'))
    if not osp.exists(remote_path):
        remote_path = canonicalize_path(remote)

    # NOTE: This has to be kept in sync with spack/store.py!
    layout = spack.directory_layout.YamlDirectoryLayout(
        remote_path,
        hash_len=config.get('install_hash_length'),
        path_scheme=config.get('install_path_scheme'))

    num_packages = 0

    for spec in filter_exclude(layout.all_specs(), exclude):
        src = layout.path_for_spec(spec)
        tgt = spack.store.layout.path_for_spec(spec)
        if osp.exists(tgt):
            if not (nostack or hardlinks):
                if osp.islink(tgt):
                    os.remove(tgt)
                else:
                    tty.warn("Cannot not stack {0} because {1} exists.".format(
                        src, tgt))
                    continue
            else:
                tty.info("Not stacking {0} because already present.".format(
                    src))
        fs.mkdirp(osp.dirname(tgt))
        tty.debug("Linking {0} -> {1}".format(src, tgt))
        if not hardlinks:
            os.symlink(src, tgt)
        else:
            os.link(src, tgt)
        num_packages += 1

    tty.info("Added {0} packages from {1}".format(num_packages, remote))

    return num_packages


def stack(parser, args):
    "Returns number of packages stacked."

    num_packages = sum((
        add_remote_packages(
            remote,
            exclude=args.exclude,
            nostack=args.nostack,
            hardlinks=args.hardlinks)
        for remote in args.remotes))

    # include the newly linked specs in the database
    spack.store.db.reindex(spack.store.layout)

    if num_packages == 0:
        tty.error("Did not link any packages, make sure the remote spack "
                  "repository does not differ in hash length or path scheme!")
    else:
        tty.info("Added {0} packages in total.".format(num_packages))

    return num_packages
