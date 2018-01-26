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

import glob
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
section = "environment"
level = "short" # TODO: re-check what 'level' is supposed to mean

def setup_parser(sp):
    setup_parser.parser = sp

    sp.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help="If not verbose only warnings/errors will be printed.")
    sp.add_argument(
        '-e', '--exclude', action='append', default=[],
        help="exclude packages with names matching the given regex pattern")

    sp.add_argument("remotes", nargs="+",
                    metavar='remote', action='store',
                    help="one or more remote spack repositories which "
                         "contain packages to be added as external packages")


def add_remote_packages(remote, exclude=[], verbose=False):
    """
        Add all installed packages in `remote` to the packages dictionary.
    """
    config = spack.config.get_config("config")

    # NOTE: This has to be kept in sync with spack/store.py!
    layout = spack.directory_layout.YamlDirectoryLayout(
        canonicalize_path(osp.join(remote, 'opt', 'spack')),
        hash_len=config.get('install_hash_length'),
        path_scheme=config.get('install_path_scheme'))

    num_packages = 0

    for spec in filter_exclude(layout.all_specs(), exclude):
        src = layout.path_for_spec(spec)
        tgt = spack.store.layout.path_for_spec(spec)
        if osp.exists(tgt):
            if osp.islink(tgt):
                os.remove(tgt)
            else:
                tty.warn("Cannot not stack {} because {} exists.".format(
                    src, tgt))
                continue
        fs.mkdirp(osp.dirname(tgt))
        if verbose:
            tty.debug("Linking {} -> {}".format(src, tgt))
        os.symlink(src, tgt)
        num_packages += 1

    if verbose:
        tty.info("Added {} packages from {}".format(num_packages, remote))

    return num_packages


def stack(parser, args):

    num_packages = sum((add_remote_packages(
            remote,
            exclude=args.exclude, verbose=args.verbose)
        for remote in args.remotes))

    spack.store.db.reindex(spack.store.layout)

    if args.verbose:
        tty.info("Added {} packages.".format(num_packages))


