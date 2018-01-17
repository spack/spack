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


class Intel(IntelPackage):
    """Intel Compilers."""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    version('18.0.1', '28cb807126d713350f4aa6f9f167448a',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12381/parallel_studio_xe_2018_update1_composer_edition.tgz')
    version('18.0.0', '31ba768fba6e7322957b03feaa3add28',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12067/parallel_studio_xe_2018_composer_edition.tgz')
    version('17.0.4', 'd03d351809e182c481dc65e07376d9a2',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11541/parallel_studio_xe_2017_update4_composer_edition.tgz')
    version('17.0.3', '52344df122c17ddff3687f84ceb21623',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11464/parallel_studio_xe_2017_update3_composer_edition.tgz')
    version('17.0.2', '2891ab1ece43eb61b6ab892f07c47f01',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11302/parallel_studio_xe_2017_update2_composer_edition.tgz')
    version('17.0.1', '1f31976931ed8ec424ac7c3ef56f5e85',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10978/parallel_studio_xe_2017_update1_composer_edition.tgz')
    version('17.0.0', 'b67da0065a17a05f110ed1d15c3c6312',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9656/parallel_studio_xe_2017_composer_edition.tgz')
    version('16.0.4', '2bc9bfc9be9c1968a6e42efb4378f40e',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9785/parallel_studio_xe_2016_composer_edition_update4.tgz')
    version('16.0.3', '3208eeabee951fc27579177b593cefe9',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9063/parallel_studio_xe_2016_composer_edition_update3.tgz')
    version('16.0.2', '1133fb831312eb519f7da897fec223fa',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8680/parallel_studio_xe_2016_composer_edition_update2.tgz')

    variant('rpath', default=True, description='Add rpath to .cfg files')

    components = [
        # Common files
        'intel-comp-',
        'intel-openmp',

        # C/C++
        'intel-icc',

        # Fortran
        'intel-ifort',
    ]

    @property
    def license_files(self):
        return [
            'Licenses/license.lic',
            join_path('compilers_and_libraries', 'linux', 'bin',
                      'intel64', 'license.lic')
        ]

    @run_after('install')
    def rpath_configuration(self):
        if '+rpath' in self.spec:
            bin_dir = join_path(self.prefix, 'compilers_and_libraries',
                                'linux', 'bin', 'intel64')
            lib_dir = join_path(self.prefix, 'compilers_and_libraries',
                                'linux', 'compiler', 'lib', 'intel64_lin')
            for compiler in ['icc', 'icpc', 'ifort']:
                cfgfilename = join_path(bin_dir, '{0}.cfg'.format(compiler))
                with open(cfgfilename, 'w') as f:
                    f.write('-Xlinker -rpath -Xlinker {0}\n'.format(lib_dir))

    def setup_environment(self, spack_env, run_env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source bin/compilervars.sh intel64
        """
        # NOTE: Spack runs setup_environment twice, once pre-build to set up
        # the build environment, and once post-installation to determine
        # the environment variables needed at run-time to add to the module
        # file. The script we need to source is only present post-installation,
        # so check for its existence before sourcing.
        # TODO: At some point we should split setup_environment into
        # setup_build_environment and setup_run_environment to get around
        # this problem.
        compilervars = os.path.join(self.prefix.bin, 'compilervars.sh')

        if os.path.isfile(compilervars):
            run_env.extend(EnvironmentModifications.from_sourcing_file(
                compilervars, 'intel64'))
