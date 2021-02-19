# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


releases = {'2021.1.2':
            {'irc_id': '17508', 'build': '62'}}


class IntelOneapiFortran(IntelOneApiCompilerPackage):
    """Intel oneAPI fortran compilers

    Contains ifort, ifx

    """

    maintainers = ['rscohn2', 'frankwillmore']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/fortran-compiler.html'

    version('2021.1.2', sha256='29345145268d08a59fa7eb6e58c7522768466dd98f6d9754540d1a0803596829', expand=False)

    variant('compiler', values=('ifort', 'ifx'), default='ifort', description='Compiler to use for FC/F77/F90')

    def __init__(self, spec):
        self.component_info(
            dir_name='compiler',
            components='all',
            releases=releases,
            url_name='fortran-compiler')
        super(IntelOneapiFortran, self).__init__(spec)

    def setup_run_environment(self, env):
        super(IntelOneapiFortran, self).setup_run_environment(env)

        if self.spec.variants['compiler'].value == 'ifort':
            fc = self._join_prefix('bin/intel64/ifort')
        elif self.spec.variants['compiler'].value == 'ifx':
            fc = self._join_prefix('bin/ifx')

        env.set('FC', fc)
        env.set('F77', fc)
        env.set('F90', fc)

        env.set('I_MPI_FC', fc)
