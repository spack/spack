##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import os

from spack import *
from spack.environment import EnvironmentModifications


class IntelDaal(IntelPackage):
    """Intel Data Analytics Acceleration Library."""

    homepage = "https://software.intel.com/en-us/daal"

    version('2018.1.163', '12a9586734a03a956095440161fd741a',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_daal_2018.1.163.tgz")
    version('2018.0.128', '5779e670f67c33cc1c6cdcdca5e4636e',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12072/l_daal_2018.0.128.tgz")
    version('2017.4.239', 'b47e9b92d948ee312e8a98170a1c0640',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12148/l_daal_2017.4.239.tgz")
    version('2017.3.196', '93221eaeb560917a129d42fb2cf02500',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11546/l_daal_2017.3.196.tgz")
    version('2017.2.174', 'f067d5d7b0f70914fba1f78da0361065',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11308/l_daal_2017.2.174.tgz")
    version('2017.1.132', '56eef8cc45219f92a27de03ae914eba4',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10983/l_daal_2017.1.132.tgz")
    version('2017.0.098', 'b4eb234de12beff4a5cba4b81ea60673',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9664/l_daal_2017.0.098.tgz")
    version('2016.3.210', 'ad747c0dd97dace4cad03cf2266cad28',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9099/l_daal_2016.3.210.tgz")
    version('2016.2.181', 'aad2aa70e5599ebfe6f85b29d8719d46',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8687/l_daal_2016.2.181.tgz")

    provides('daal')

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

           $ source daal/bin/daalvars.sh intel64
        """
        # NOTE: Spack runs setup_environment twice, once pre-build to set up
        # the build environment, and once post-installation to determine
        # the environment variables needed at run-time to add to the module
        # file. The script we need to source is only present post-installation,
        # so check for its existence before sourcing.
        # TODO: At some point we should split setup_environment into
        # setup_build_environment and setup_run_environment to get around
        # this problem.
        daalvars = os.path.join(self.prefix.daal.bin, 'daalvars.sh')

        if os.path.isfile(daalvars):
            run_env.extend(EnvironmentModifications.from_sourcing_file(
                daalvars, 'intel64'))
