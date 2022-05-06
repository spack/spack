# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack import *


class IntelOneapiAdvisor(IntelOneApiPackage):
    __doc__ = ("""Intel® Advisor™ is a design and analysis tool for developing
    performant code. The tool supports C, C++, Fortran, SYCL*,
    OpenMP*, OpenCL™ code, and Python*. It helps with the following:
    Performant CPU Code: Design your application for efficient
    threading, vectorization, and memory use. Efficient GPU Offload:
    Identify parts of the code that can be profitably
    offloaded. Optimize the code for compute and memory."""
               + IntelOneApiPackage.license_text)

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/advisor.html'

    if platform.system() == 'Linux':
        version('2022.1.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18730/l_oneapi_advisor_p_2022.1.0.171_offline.sh',
                sha256='b627dbfefa779b44e7ab40dfa37614e56caa6e245feaed402d51826e6a7cb73b',
                expand=False)
        version('2022.0.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18369/l_oneapi_advisor_p_2022.0.0.92_offline.sh',
                sha256='f1c4317c2222c56fb2e292513f7eec7ec27eb1049d3600cb975bc08ed1477993',
                expand=False)
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18220/l_oneapi_advisor_p_2021.4.0.389_offline.sh',
                sha256='dd948f7312629d9975e12a57664f736b8e011de948771b4c05ad444438532be8',
                expand=False)

    @property
    def component_dir(self):
        return 'advisor'
