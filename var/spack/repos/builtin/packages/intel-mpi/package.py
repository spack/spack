# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelMpi(IntelPackage):
    """Intel MPI"""

    homepage = "https://software.intel.com/en-us/intel-mpi-library"

    version('2019.4.243', '233a8660b92ecffd89fedd09f408da6ee140f97338c293146c9c080a154c5fcd',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15553/l_mpi_2019.4.243.tgz')
    version('2019.3.199', '5304346c863f64de797250eeb14f51c5cfc8212ff20813b124f20e7666286990',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15260/l_mpi_2019.3.199.tgz')
    version('2019.1.144', 'dac86a5db6b86503313742b17535856a432955604f7103cb4549a9bfc256c3cd',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14879/l_mpi_2019.1.144.tgz')
    version('2019.0.117', '8572d5fa1f26a7de8edc8b64653b0955',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13584/l_mpi_2019.0.117.tgz')
    version('2018.4.274', 'a1114b3eb4149c2f108964b83cad02150d619e50032059d119ac4ffc9d5dd8e0',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13741/l_mpi_2018.4.274.tgz')
    version('2018.3.222', 'df92593818fadff63c57418669c6083b',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13112/l_mpi_2018.3.222.tgz')
    version('2018.2.199', '6ffeab59c83a8842537484d53e180520',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12748/l_mpi_2018.2.199.tgz')
    version('2018.1.163', '437ce50224c5bbf98fd578a810c3e401',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_mpi_2018.1.163.tgz')
    version('2018.0.128', '15b46fc6a3014595de897aa48d3a658b',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12120/l_mpi_2018.0.128.tgz')
    version('2017.4.239', '460a9ef1b3599d60b4d696e3f0f2a14d',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12209/l_mpi_2017.4.239.tgz')
    version('2017.3.196', '721ecd5f6afa385e038777e5b5361dfb',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11595/l_mpi_2017.3.196.tgz')
    version('2017.2.174', 'b6c2e62c3fb9b1558ede72ccf72cf1d6',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11334/l_mpi_2017.2.174.tgz')
    version('2017.1.132', 'd5e941ac2bcf7c5576f85f6bcfee4c18',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11014/l_mpi_2017.1.132.tgz')
    # built from parallel_studio_xe_2016.3.068
    version('5.1.3.223',  '4316e78533a932081b1a86368e890800',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9278/l_mpi_p_5.1.3.223.tgz')

    provides('mpi')

    def setup_dependent_environment(self, *args):
        # Handle in callback, conveying client's compilers in additional arg.
        # CAUTION - DUP code in:
        #   ../intel-mpi/package.py
        #   ../intel-parallel-studio/package.py
        self._setup_dependent_env_callback(*args, compilers_of_client={
            'CC':   spack_cc,
            'CXX':  spack_cxx,
            'F77':  spack_f77,
            'F90':  spack_fc,
            'FC':   spack_fc,
        })
