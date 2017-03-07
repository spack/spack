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
from __future__ import absolute_import

import os
import re
import platform

from llnl.util.filesystem import *

import spack
from spack.util.executable import *


def pre_run():
    if platform.system() != "Darwin":
        return

    git_case_consistency_check(spack.repo.get_repo('builtin').packages_path)


def git_case_consistency_check(path):
    """Re-sync case of files in a directory with git.

    On case-insensitive but case-preserving filesystems like Mac OS X,
    Git doesn't properly rename files that only had their case changed.

    This checks files in a directory against git and does a
    case-restoring rename (actually two renames, e.g.::

        name -> tmp -> NAME

    We use this in Spack to ensure package directories are named
    correctly.

    TODO: this check can probably be removed once package names have been
    TODO: lowercase for a long while.

    """
    with working_dir(path):
        # Don't bother fixing case if Spack isn't in a git repository
        git = which('git')
        if not git:
            return

        try:
            git_filenames = git('ls-tree', '--name-only', 'HEAD', output=str)
            git_filenames = set(re.split(r'\s+', git_filenames.strip()))
        except ProcessError:
            return  # Ignore errors calling git

        lower_to_mixed = {}
        for fn in git_filenames:
            lower = fn.lower()
            mixed = lower_to_mixed.setdefault(lower, [])
            mixed.append(fn)

        # Iterate through all actual files and make sure their names are
        # the same as corresponding names in git
        actual_filenames = os.listdir('.')
        for actual in actual_filenames:
            lower = actual.lower()

            # not tracked by git
            if lower not in lower_to_mixed:
                continue

            # Don't know what to do with multiple matches
            if len(lower_to_mixed[lower]) != 1:
                continue

            # Skip if case is already correct
            git_name = lower_to_mixed[lower][0]
            if git_name == actual:
                continue

            # restore case with two renames
            tmp_name = actual + '.spack.tmp'
            os.rename(actual, tmp_name)
            os.rename(tmp_name, git_name)
