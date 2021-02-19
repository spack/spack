# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


releases = {'2021.1.2':
            {'irc_id': '17513', 'build': '63'}}


class IntelOneapiCpp(IntelOneApiCompilerPackage):
    """Intel oneAPI C++ compilers.

    Contains icc, icpc, icx, icpx, dpcpp.

    """

    maintainers = ['rscohn2', 'frankwillmore']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/dpc-compiler.html'

    version('2021.1.2', sha256='68d6cb638091990e578e358131c859f3bbbbfbf975c581fd0b4b4d36476d6f0a', expand=False)

    variant('compiler', values=('icc', 'icx', 'dpcpp'), default='icc', description='Compiler family to use for CC/CXX')

    def __init__(self, spec):
        self.component_info(
            dir_name='compiler',
            components='all',
            releases=releases,
            url_name='dpcpp-cpp-compiler')
        super(IntelOneapiCpp, self).__init__(spec)

    def setup_run_environment(self, env):
        super(IntelOneapiCpp, self).setup_run_environment(env)

        icc = self._join_prefix('bin/intel64/icc')
        icpc = self._join_prefix('bin/intel64/icpc')
        icx = self._join_prefix('bin/icx')
        icpx = self._join_prefix('bin/icpx')
        dpcpp = self._join_prefix('bin/dpcpp')

        if self.spec.variants['compiler'].value == 'icc':
            cc = icc
            cxx = icpc
        elif self.spec.variants['compiler'].value == 'icx':
            cc = icx
            cxx = icpx
        elif self.spec.variants['compiler'].value == 'dpcpp':
            cc = icx
            cxx = dpcpp
        else:
            assert False

        env.set('CC', cc)
        env.set('CXX', cxx)
        # Set these so that MPI wrappers will pick up these compilers
        # when this module is loaded.
        env.set('I_MPI_CC', cc)
        env.set('I_MPI_CXX', cxx)
