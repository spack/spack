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


class Librom(AutotoolsPackage):
    """libROM: library for computing large-scale reduced order models"""

    homepage = "https://github.com/LLNL/libROM"
    git      = "https://github.com/LLNL/libROM.git"

    version('develop', branch='master')

    depends_on('lapack')
    depends_on('mpi')
    depends_on('zlib')
    depends_on('libszip')
    depends_on('hdf5')
    depends_on('perl')
    depends_on('graphviz')
    depends_on('doxygen')
    depends_on('boost')

    def configure_args(self):
        spec = self.spec
        args = ['--with-lapack={0}'.format(spec['lapack'].prefix),
                '--with-lapack-libs={0}'.format(spec['lapack'].libs.ld_flags),
                '--with-zlib={0}'.format(spec['zlib'].prefix),
                '--with-szlib={0}'.format(spec['libszip'].prefix),
                '--with-hdf5={0}'.format(spec['hdf5'].prefix),
                '--with-MPICC={0}'.format(spec['mpi'].mpicc),
                '--with-mpi-include={0}'.format(spec['mpi'].prefix.include),
                '--with-mpi-libs={0}'.format(spec['mpi'].libs.ld_flags),
                '--with-perl={0}'.format(spec['perl'].prefix),
                '--with-doxygen={0}'.format(spec['doxygen'].prefix)]
        return args

    # TODO(oxberry1@llnl.gov): Submit PR upstream that implements
    # install phase in autotools
    def install(self, spec, prefix):
        mkdirp(self.spec.prefix.lib)
        install('libROM.a', join_path(self.spec.prefix.lib, 'libROM.a'))

        mkdirp(self.spec.prefix.include)
        for f in glob.glob('*.h'):
            install(f, join_path(self.spec.prefix.include, f))

        mkdirp(self.spec.prefix.share)
        install('libROM_Design_and_Theory.pdf',
                join_path(self.spec.prefix.share,
                          'libROM_Design_and_Theory.pdf'))

        install_tree('docs', self.spec.prefix.share.docs)
