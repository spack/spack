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
import glob
import os.path


class Xbraid(MakefilePackage):
    """XBraid: Parallel time integration with Multigrid"""

    homepage = "https://computation.llnl.gov/projects/parallel-time-integration-multigrid/software"
    url      = "https://computation.llnl.gov/projects/parallel-time-integration-multigrid/download/braid_2.2.0.tar.gz"

    version('2.2.0', '0a9c2fc3eb8f605f73cce78ab0d8a7d9')

    depends_on('mpi')

    def build(self, spec, prefix):
        make('libbraid.a')

    # XBraid doesn't have a real install target, so it has to be done
    # manually
    def install(self, spec, prefix):
        # Install headers
        mkdirp(prefix.include)
        headers = glob.glob('*.h')
        for f in headers:
            install(f, join_path(prefix.include, os.path.basename(f)))

        # Install library
        mkdirp(prefix.lib)
        library = 'libbraid.a'
        install(library, join_path(prefix.lib, library))

        # Install other material (e.g., examples, tests, docs)
        mkdirp(prefix.share)
        install('makefile.inc', prefix.share)
        install_tree('examples', prefix.share.examples)
        install_tree('drivers', prefix.share.drivers)

        # TODO: Some of the scripts in 'test' are useful, even for
        # users; some could be deleted from an installation because
        # they're not useful to users
        install_tree('test', prefix.share.test)
        install_tree('user_utils', prefix.share.user_utils)
        install_tree('docs', prefix.share.docs)

    @property
    def libs(self):
        return find_libraries('libbraid', root=self.prefix,
                              shared=False, recursive=True)
