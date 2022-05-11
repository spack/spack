# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Exawind(CMakePackage):
    """Multi-application driver for Exawind project."""

    homepage = "https://github.com/Exawind/exawind-driver"
    git = "https://github.com/Exawind/exawind-driver.git"

    maintainers = ['jrood-nrel']

    tags = ['ecp', 'ecp-apps']

    version('master', branch='main')

    depends_on('trilinos+stk')
    depends_on('tioga+shared~nodegid')
    depends_on('nalu-wind+hypre+openfast+tioga+wind-utils')
    depends_on('amr-wind+hypre+mpi+netcdf+openfast')
    depends_on('openfast+cxx+shared@2.6.0:')
    depends_on('yaml-cpp@0.6:')

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define('Trilinos_DIR', spec['trilinos'].prefix),
            self.define('TIOGA_DIR', spec['tioga'].prefix),
            self.define('Nalu-Wind_DIR', spec['nalu-wind'].prefix),
            self.define('AMR-Wind_DIR', spec['amr-wind'].prefix),
            self.define('OpenFAST_DIR', spec['openfast'].prefix),
            self.define('YAML-CPP_DIR', spec['yaml-cpp'].prefix)
        ]

        return args
