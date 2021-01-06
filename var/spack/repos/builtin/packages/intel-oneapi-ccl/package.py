# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

releases = {
    '2021.1.1': {'irc_id': '17391', 'build': '54'}}


class IntelOneapiCcl(IntelOneApiLibraryPackage):
    """Intel oneAPI CCL."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/oneccl.html'

    version('2021.1.1', sha256='de732df57a03763a286106c8b885fd60e83d17906936a8897a384b874e773f49', expand=False)

    def __init__(self, spec):
        self.component_info(dir_name='ccl',
                            components='intel.oneapi.lin.ccl.devel',
                            releases=releases,
                            url_name='oneapi_ccl')
        super(IntelOneapiCcl, self).__init__(spec)
