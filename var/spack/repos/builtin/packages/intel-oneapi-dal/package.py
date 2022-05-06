# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import platform

from spack import *


class IntelOneapiDal(IntelOneApiLibraryPackage):
    __doc__ = ("""Intel® Data Analytics Library (DAL) provides the right tools to
    build compute-intense applications that run fast on Intel®
    architecture. It includes algorithms for analysis functions, math
    functions, training and library prediction functions for C++ and
    Java*."""
               + IntelOneApiPackage.license_text)

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onedal.html'

    if platform.system() == 'Linux':
        version('2021.6.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18698/l_daal_oneapi_p_2021.6.0.915_offline.sh',
                sha256='bc9a430f372a5f9603c19ec25207c83ffd9d59fe517599c734d465e32afc9790',
                expand=False)
        version('2021.5.3',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18480/l_daal_oneapi_p_2021.5.3.832_offline.sh',
                sha256='6d3503cf7be2908bbb7bd18e67b8f2e96ad9aec53d4813c9be620adaa2db390f',
                expand=False)
        version('2021.5.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18432/l_daal_oneapi_p_2021.5.1.803_offline.sh',
                sha256='bba7bee3caef14fbb54ad40615222e5da429496455edf7375f11fd84a72c87ba',
                expand=False)
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18218/l_daal_oneapi_p_2021.4.0.729_offline.sh',
                sha256='61da9d2a40c75edadff65d052fd84ef3db1da5d94f86ad3956979e6988549dda',
                expand=False)
        version('2021.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17905/l_daal_oneapi_p_2021.3.0.557_offline.sh',
                sha256='4c2e77a3a2fa5f8a09b7d68760dfca6c07f3949010836cd6da34075463467995',
                expand=False)
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17747/l_daal_oneapi_p_2021.2.0.358_offline.sh',
                sha256='cbf4e64dbd21c10179f2d1d7e8b8b0f12eeffe6921602df33276cd0ebd1f8e34',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17443/l_daal_oneapi_p_2021.1.1.79_offline.sh',
                sha256='6e0e24bba462e80f0fba5a46e95cf0cca6cf17948a7753f8e396ddedd637544e',
                expand=False)

    depends_on('intel-oneapi-tbb')

    provides('daal')
    provides('onedal')

    @property
    def component_dir(self):
        return 'dal'
