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
"""Creates various objects that are part of Spack Core according to the
options specified in the configuration files.

This module has been created to have a single place in which we mix the
information stemming from the yaml configuration files with the business
logic coded in other parts of Spack's core.
"""

import llnl.util.tty as tty
import spack.config
import spack.repository


def make_repo_path_from_config():
    """Creates an instance of RepoPath reading the directories where the
    repositories are located from Spack configuration files.
    """

    repo_dirs = spack.config.get_config('repos')

    msg = '[REPOSITORY] Creating RepoPath from configuration files: {0}'
    tty.debug(msg.format(repo_dirs))

    if not repo_dirs:
        msg = 'Spack configuration contains no package repositories.'
        raise spack.repository.NoRepoConfiguredError(msg)

    return spack.repository.RepoPath(*repo_dirs)
