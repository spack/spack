# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


releases = {'2021.1.0':
            {'irc_id': '17427', 'build': '2684'}}


class IntelOneapiCompilers(IntelOneApiPackage):
    '''Intel oneAPI compilers.

    Contains icc, icpc, icx, icpx, dpcpp, ifort, ifx.

    '''

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/dpc-compiler.html'

    version('2021.1.0', sha256='666b1002de3eab4b6f3770c42bcf708743ac74efeba4c05b0834095ef27a11b9', expand=False)

    def __init__(self, spec):
        self.component_info(
            dir_name='compiler',
            components=('intel.oneapi.lin.dpcpp-cpp-compiler-pro'
                        ':intel.oneapi.lin.ifort-compiler'),
            releases=releases,
            url_name='HPCKit')
        super(IntelOneapiCompilers, self).__init__(spec)
