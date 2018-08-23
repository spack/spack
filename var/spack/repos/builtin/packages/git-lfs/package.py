##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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
from spack import *


class GitLfs(Package):
    """Git LFS is a system for managing and versioning large files in
       association with a Git repository.  Instead of storing the large files
       within the Git repository as blobs, Git LFS stores special "pointer
       files" in the repository, while storing the actual file contents on a
       Git LFS server."""

    homepage = "https://git-lfs.github.com"
    git      = "https://github.com/github/git-lfs.git"

    version('2.3.0', tag='v2.3.0')
    version('2.2.1', tag='v2.2.1')
    version('2.0.2', tag='v2.0.2')
    version('1.4.1', tag='v1.4.1')
    version('1.3.1', tag='v1.3.1')

    # TODO: Add tests by following the instructions at this location:
    # https://github.com/github/git-lfs/blob/master/CONTRIBUTING.md#building

    depends_on('go@1.5:', type='build')
    depends_on('git@1.8.2:', type='run')

    def install(self, spec, prefix):
        bootstrap_script = Executable(join_path('script', 'bootstrap'))
        bootstrap_script()

        mkdirp(prefix.bin)
        install(join_path('bin', 'git-lfs'), prefix.bin)
