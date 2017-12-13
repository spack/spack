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
from spack import *


class Laghos(MakefilePackage):
    """Laghos (LAGrangian High-Order Solver) is a CEED miniapp that solves the
       time-dependent Euler equations of compressible gas dynamics in a moving
       Lagrangian frame using unstructured high-order finite element spatial
       discretization and explicit high-order time-stepping.
    """
    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "https://codesign.llnl.gov/laghos.php"
    git      = "https://github.com/CEED/Laghos"
    url      = "https://github.com/CEED/Laghos/archive/v1.0.tar.gz"

    version('1.0', '4c091e115883c79bed81c557ef16baff')
    version('develop', git=git, branch='master')

    depends_on('mpi')
    depends_on('mfem@laghos-v1.0', when='@1.0')

    @property
    def build_targets(self):
        targets = []
        spec = self.spec

        targets.append('MFEM_DIR=%s' % spec['mfem'].prefix)
        targets.append('CONFIG_MK=%s' % join_path(spec['mfem'].prefix,
                       'share/mfem/config.mk'))
        targets.append('TEST_MK=%s' % join_path(spec['mfem'].prefix,
                       'share/mfem/test.mk'))
        targets.append('CXX=%s' % spec['mpi'].mpicxx)

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('laghos', prefix.bin)
