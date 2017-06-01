##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack.util.prefix import Prefix
from spack import *


class IntelIpp(IntelPackage):
    """Intel Integrated Performance Primitives."""

    homepage = "https://software.intel.com/en-us/intel-ipp"

    version('2017.3.196', '47e53bd1a2740041f4d0be7c36b61a18',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11545/l_ipp_2017.3.196.tgz")
    version('2017.2.174', '8ad7753ee30c5176c4931070334144bc',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11307/l_ipp_2017.2.174.tgz")
    version('2017.1.132', '9fbbaa402b8d16f4cb4be9aee2f557c2',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11031/l_ipp_2017.1.132.tgz")
    version('2017.0.098', 'e7be757ebe351d9f9beed7efdc7b7118',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9663/l_ipp_2017.0.098.tgz")
    version('9.0.3.210', '0e1520dd3de7f811a6ef6ebc7aa429a3',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9067/l_ipp_9.0.3.210.tgz")

    provides('ipp')

    @property
    def license_required(self):
        # The Intel libraries are provided without requiring a license as of
        # version 2017.2. Trying to specify the license will fail. See:
        # https://software.intel.com/en-us/articles/free-ipsxe-tools-and-libraries
        if self.version >= Version('2017.2'):
            return False
        else:
            return True

    def setup_environment(self, spack_env, run_env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source ipp/bin/ippvars.sh intel64
        """
        ipp_root = Prefix(join_path(self.prefix, 'ipp'))

        run_env.prepend_path('CPATH', ipp_root.include)
        run_env.prepend_path('IPPROOT', ipp_root)
        run_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(ipp_root.lib, 'intel64'))
        run_env.prepend_path('LIBRARY_PATH',
                             join_path(ipp_root.lib, 'intel64'))
        run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                             join_path(ipp_root.lib, 'mic'))
