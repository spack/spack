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
from spack import *


class GitLfs(Package):
    """Tool for managing large files with Git."""

    homepage = "https://git-lfs.github.com"
    url      = "https://github.com/github/git-lfs/archive/v1.4.1.tar.gz"

    version('1.4.1', 'c62a314d96d3a30af4d98fa3305ad317')

    depends_on('go@1.5:', type='build')
    depends_on('git@1.8.2:', type='run')

    def install(self, spec, prefix):
        bootstrap = Executable('./scripts/bootstrap')
        bootstrap()
        install('bin/git-lfs', prefix.bin)
