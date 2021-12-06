# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import platform

from spack import *


class IntelOneapiIppcp(IntelOneApiLibraryPackage):
    """Intel oneAPI IPP Crypto."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/ipp.html'

    if platform.system() == 'Linux':
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18187/l_ippcp_oneapi_p_2021.4.0.401_offline.sh',
                sha256='2ca2320f733ee75b4a27865185a1b0730879fe2c47596e570b1bd50d0b8ac608',
                expand=False)
        version('2021.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17886/l_ippcp_oneapi_p_2021.3.0.315_offline.sh',
                sha256='0214d132d8e64b02e9cc63182e2099fb9caebf8c240fb1629ae898c2e1f72fb9',
                expand=False)
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17684/l_ippcp_oneapi_p_2021.2.0.231_offline.sh',
                sha256='64cd5924b42f924b6a8128a8bf8e686f5dc52b98f586ffac6c2e2f1585e3aba9',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17415/l_ippcp_oneapi_p_2021.1.1.54_offline.sh',
                sha256='c0967afae22c7a223ec42542bcc702121064cd3d8f680eff36169c94f964a936',
                expand=False)

    @property
    def component_dir(self):
        return 'ippcp'
