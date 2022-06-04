# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiDpct(IntelOneApiPackage):
    """Intel oneAPI DPC++ Compatibility Tool."""

    maintainers = ['rscohn2']

    homepage = 'https://www.intel.com/content/www/us/en/developer/tools/oneapi/dpc-compatibility-tool.html#gs.2p8km6'

    if platform.system() == 'Linux':
        version('2022.1.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18746/l_dpcpp-ct_p_2022.1.0.172_offline.sh',
                sha256='ec42f4df3f9daf1af587b14b8b6644c773a0b270e03dd22ac9e2f49131e3e40c',
                expand=False)

    @property
    def component_dir(self):
        return 'dpcpp-ct'
