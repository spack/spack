# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class IntelMkl(IntelPackage):
    """Intel Math Kernel Library."""

    homepage = "https://software.intel.com/en-us/intel-mkl"

    version('2019.3.199', '06de2b54f4812e7c39a118536259c942029fe1d6d8918ad9df558a83c4162b8f',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15275/l_mkl_2019.3.199.tgz")
    version('2019.1.144', '5205a460a9c685f7a442868367389b2d0c25e1455346bc6a37c5b8ff90a20fbb',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14895/l_mkl_2019.1.144.tgz")
    version('2019.0.117', 'd9e1b6b96fbffd4b306c7e8291f141a2',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13575/l_mkl_2019.0.117.tgz")
    version('2018.4.274', '18eb3cde3e6a61a88f25afff25df762a560013f650aaf363f7d3d516a0d04881',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13725/l_mkl_2018.4.274.tgz")
    version('2018.3.222', '3e63646a4306eff95e8d0aafd53a2983',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13005/l_mkl_2018.3.222.tgz")
    version('2018.2.199', 'fd31b656a8eb859c89495b9cc41230b4',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12725/l_mkl_2018.2.199.tgz")
    version('2018.1.163', 'f1f7b6ddd7eb57dfe39bd4643446dc1c',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_mkl_2018.1.163.tgz")
    version('2018.0.128', '0fa23779816a0f2ee23a396fc1af9978',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12070/l_mkl_2018.0.128.tgz")
    version('2017.4.239', '3066272dd0ad3da7961b3d782e1fab3b',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12147/l_mkl_2017.4.239.tgz")
    version('2017.3.196', '4a2eb4bee789391d9c07d7c348a80702',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11544/l_mkl_2017.3.196.tgz")
    version('2017.2.174', 'ef39a12dcbffe5f4a0ef141b8759208c',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11306/l_mkl_2017.2.174.tgz")
    version('2017.1.132', '7911c0f777c4cb04225bf4518088939e',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11024/l_mkl_2017.1.132.tgz")
    version('2017.0.098', '3cdcb739ab5ab1e047eb130b9ffdd8d0',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9662/l_mkl_2017.0.098.tgz")
    # built from parallel_studio_xe_2016.3.x
    version('11.3.3.210', 'f72546df27f5ebb0941b5d21fd804e34',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9068/l_mkl_11.3.3.210.tgz")
    # built from parallel_studio_xe_2016.2.062
    version('11.3.2.181', '536dbd82896d6facc16de8f961d17d65',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8711/l_mkl_11.3.2.181.tgz")

    variant('shared', default=True, description='Builds shared library')
    variant('ilp64', default=False, description='64 bit integers')
    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('openmp', 'tbb', 'none'),
        multi=False
    )

    provides('blas')
    provides('lapack')
    provides('scalapack')
    provides('mkl')
    provides('fftw-api@3', when='@2017:')

    if sys.platform == 'darwin':
        # there is no libmkl_gnu_thread on macOS
        conflicts('threads=openmp', when='%gcc')
