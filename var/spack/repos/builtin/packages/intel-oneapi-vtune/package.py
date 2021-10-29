# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack import *


class IntelOneapiVtune(IntelOneApiPackage):
    """Intel oneAPI VTune Profiler.
    Installed in Perf driverless mode, detailed here: https://software.intel.com/content/www/us/en/develop/documentation/vtune-cookbook/top/configuration-recipes/profiling-hardware-without-sampling-drivers.html
    Users can manually install drivers, please read the instructions here: https://software.intel.com/content/www/us/en/develop/documentation/vtune-help/top/set-up-analysis-target/linux-targets/building-and-installing-the-sampling-drivers-for-linux-targets.html
    """

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/vtune-profiler.html'

    if platform.system() == 'Linux':
        version('2021.7.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18086/l_oneapi_vtune_p_2021.7.1.492_offline.sh',
                sha256='4cf17078ae6e09f26f70bd9d0b726af234cc30c342ae4a8fda69941b40139b26',
                expand=False)
        version('2021.6.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18012/l_oneapi_vtune_p_2021.6.0.411_offline.sh',
                sha256='6b1df7da713337aa665bcc6ff23e4a006695b5bfaf71dffd305cbadca2e5560c',
                expand=False)

    @property
    def component_dir(self):
        return 'vtune'
