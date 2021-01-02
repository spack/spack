# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

releases = {
    '2021.1.1': {'irc_id': '17418', 'build': '66'}}


class IntelOneapiVpl(IntelOneApiLibraryPackage):
    """Intel oneAPI VPL."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onevpl.html'

    version('2021.1.1', sha256='0fec42545b30b7bb2e4e33deb12ab27a02900f5703153d9601673a8ce43082ed', expand=False)

    def __init__(self, spec):
        self.component_info(dir_name='vpl',
                            components='intel.oneapi.lin.vpl.devel',
                            releases=releases,
                            url_name='oneVPL')
        super(IntelOneapiVpl, self).__init__(spec)
