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


class Laghos(MakefilePackage):
    """Laghos (LAGrangian High-Order Solver) is a CEED miniapp that solves the
       time-dependent Euler equations of compressible gas dynamics in a moving
       Lagrangian frame using unstructured high-order finite element spatial
       discretization and explicit high-order time-stepping.
    """
    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "https://github.com/CEED/Laghos"
    url      = "https://github.com/CEED/Laghos/archive/v1.0.tar.gz"
    git      = "https://github.com/CEED/Laghos.git"

    version('develop', branch='master')
    version('1.0', '4c091e115883c79bed81c557ef16baff')

    variant('metis', default=True, description='Enable/disable METIS support')

    depends_on('mfem@develop+mpi+metis', when='@develop+metis')
    depends_on('mfem@develop+mpi~metis', when='@develop~metis')
    depends_on('mfem@laghos-v1.0,3.3.2:+mpi+metis', when='@1.0+metis')
    depends_on('mfem@laghos-v1.0,3.3.2:+mpi~metis', when='@1.0~metis')

    @property
    def build_targets(self):
        targets = []
        spec = self.spec

        targets.append('MFEM_DIR=%s' % spec['mfem'].prefix)
        targets.append('CONFIG_MK=%s' % spec['mfem'].package.config_mk)
        targets.append('TEST_MK=%s' % spec['mfem'].package.test_mk)
        targets.append('CXX=%s' % spec['mpi'].mpicxx)

        return targets

    # See lib/spack/spack/build_systems/makefile.py
    def check(self):
        targets = []
        spec = self.spec

        targets.append('MFEM_DIR=%s' % spec['mfem'].prefix)
        targets.append('CONFIG_MK=%s' % spec['mfem'].package.config_mk)
        targets.append('TEST_MK=%s' % spec['mfem'].package.test_mk)

        with working_dir(self.build_directory):
            make('test', *targets)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('laghos', prefix.bin)
