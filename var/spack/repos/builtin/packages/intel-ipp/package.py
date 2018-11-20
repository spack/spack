# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelIpp(IntelPackage):
    """Intel Integrated Performance Primitives."""

    homepage = "https://software.intel.com/en-us/intel-ipp"

    version('2019.1.144', '1eb7cd0fba74615aeafa4e314c645414497eb73f1705200c524fe78f00620db3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14887/l_ipp_2019.1.144.tgz')
    version('2019.0.117', 'c96be6e138d32bf9b8abc789d25db71d',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13576/l_ipp_2019.0.117.tgz')
    version('2018.4.274', 'bdc6082c65410c98ccf6daf239e0a6625d15ec5e0ddc1c0563aad42b6ba9063c',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13726/l_ipp_2018.4.274.tgz')
    version('2018.3.222', '2ccc16ec002466e52f1e6e1bfe9b1149',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13006/l_ipp_2018.3.222.tgz')
    version('2018.2.199', 'f87276b485d2f6ec070c1b41ac1ed871',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12726/l_ipp_2018.2.199.tgz')
    version('2018.1.163', '183d4888f3d91f632b617fdd401f04ed',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_ipp_2018.1.163.tgz')
    version('2018.0.128', 'e64190bc9041b52d9eed7e8ee91bf1de',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12071/l_ipp_2018.0.128.tgz')
    version('2017.3.196', '47e53bd1a2740041f4d0be7c36b61a18',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11545/l_ipp_2017.3.196.tgz")
    version('2017.2.174', '8ad7753ee30c5176c4931070334144bc',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11307/l_ipp_2017.2.174.tgz")
    version('2017.1.132', '9fbbaa402b8d16f4cb4be9aee2f557c2',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11031/l_ipp_2017.1.132.tgz")
    version('2017.0.098', 'e7be757ebe351d9f9beed7efdc7b7118',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9663/l_ipp_2017.0.098.tgz")
    # built from parallel_studio_xe_2016.3.067
    version('9.0.3.210', '0e1520dd3de7f811a6ef6ebc7aa429a3',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9067/l_ipp_9.0.3.210.tgz")

    provides('ipp')
