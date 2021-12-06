# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack import *


class IntelOneapiAdvisor(IntelOneApiPackage):
    """Intel Advisor is a design and analysis tool for achieving
       high application performance. This is done through
       efficient threading, vectorization, and memory use, and
       GPU offload on current and future Intel hardware."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/advisor.html'

    if platform.system() == 'Linux':
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18220/l_oneapi_advisor_p_2021.4.0.389_offline.sh',
                sha256='dd948f7312629d9975e12a57664f736b8e011de948771b4c05ad444438532be8',
                expand=False)

    @property
    def component_dir(self):
        return 'advisor'
