# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

releases = {
    '2021.1.1': {'irc_id': '17443', 'build': '79'}}


class IntelOneapiDal(IntelOneApiLibraryPackage):
    """Intel oneAPI DAL."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onedal.html'

    version('2021.1.1', sha256='6e0e24bba462e80f0fba5a46e95cf0cca6cf17948a7753f8e396ddedd637544e', expand=False)

    def __init__(self, spec):
        self.component_info(dir_name='dal',
                            components='intel.oneapi.lin.dal.devel',
                            releases=releases,
                            url_name='daal_oneapi')
        super(IntelOneapiDal, self).__init__(spec)
