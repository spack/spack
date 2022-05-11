# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.util.package import *


class IntelOneapiInspector(IntelOneApiPackage):
    """Intel Inspector is a memory and thread checking and debugging tool to increase
       the reliability, security, and accuracy of C/C++ and Fortran applications."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/inspector.html'

    if platform.system() == 'Linux':
        version('2022.0.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18363/l_inspector_oneapi_p_2022.0.0.56_offline.sh',
                sha256='79a0eb2ae3f1de1e3456076685680c468702922469c3fda3e074718fb0bea741',
                expand=False)
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18239/l_inspector_oneapi_p_2021.4.0.266_offline.sh',
                sha256='c8210cbcd0e07cc75e773249a5e4a02cf34894ec80a213939f3a20e6c5705274',
                expand=False)
        version('2021.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17946/l_inspector_oneapi_p_2021.3.0.217_offline.sh',
                sha256='1371ca74be2a6d4b069cdb3f8f2d6109abbc3261a81f437f0fe5412a7b659b43',
                expand=False)

    @property
    def component_dir(self):
        return 'inspector'
