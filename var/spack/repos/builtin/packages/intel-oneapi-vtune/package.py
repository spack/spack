# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack import *


class IntelOneapiVtune(IntelOneApiPackage):
    __doc__ = ("""Intel VTune Profiler is a profiler to optimize application
    performance, system performance, and system configuration for HPC,
    cloud, IoT, media, storage, and more.  CPU, GPU, and FPGA: Tune
    the entire application's performance--not just the accelerated
    portion. Multilingual: Profile SYCL*, C, C++, C#, Fortran, OpenCL
    code, Python*, Google Go* programming language, Java*, .NET,
    Assembly, or any combination of languages.  System or Application:
    Get coarse-grained system data for an extended period or detailed
    results mapped to source code. Power: Optimize performance while
    avoiding power and thermal-related throttling."""
               + IntelOneApiPackage.license_text)

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/vtune-profiler.html'

    if platform.system() == 'Linux':
        version('2022.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18656/l_oneapi_vtune_p_2022.3.0.195_offline.sh',
                sha256='7921fce7fcc3b82575be22d9c36beec961ba2a9fb5262ba16a04090bcbd2e1a6',
                expand=False)
        version('2022.0.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18406/l_oneapi_vtune_p_2022.0.0.94_offline.sh',
                sha256='aa4d575c22e7be0c950b87d67d9e371f470f682906864c4f9b68e530ecd22bd7',
                expand=False)
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
