# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

releases = {
    '2021.1.1': {'irc_id': '17415', 'build': '54'}}


class IntelOneapiIppcp(IntelOneApiLibraryPackage):
    """Intel oneAPI IPP Crypto."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/ipp.html'

    version('2021.1.1', sha256='c0967afae22c7a223ec42542bcc702121064cd3d8f680eff36169c94f964a936', expand=False)

    def __init__(self, spec):
        self.component_info(dir_name='ippcp',
                            components='intel.oneapi.lin.ippcp.devel',
                            releases=releases,
                            url_name='ippcp_oneapi')
        super(IntelOneapiIppcp, self).__init__(spec)
