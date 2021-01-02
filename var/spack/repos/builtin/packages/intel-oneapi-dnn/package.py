# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

releases = {
    '2021.1.1': {'irc_id': '17385', 'build': '55'}}


class IntelOneapiDnn(IntelOneApiLibraryPackage):
    """Intel oneAPI DNN."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onednn.html'

    version('2021.1.1', sha256='24002c57bb8931a74057a471a5859d275516c331fd8420bee4cae90989e77dc3', expand=False)

    def __init__(self, spec):
        self.component_info(dir_name='dnn',
                            components='intel.oneapi.lin.dnnl.devel',
                            releases=releases,
                            url_name='onednn')
        super(IntelOneapiDnn, self).__init__(spec)
