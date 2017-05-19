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
from spack import *
import os
import re


class Intel(IntelPackage):
    """Intel Compilers."""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    version('17.0.4', 'd03d351809e182c481dc65e07376d9a2',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11541/parallel_studio_xe_2017_update4_composer_edition.tgz')
    version('17.0.3', '52344df122c17ddff3687f84ceb21623',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11464/parallel_studio_xe_2017_update3_composer_edition.tgz')
    version('17.0.2',     '2891ab1ece43eb61b6ab892f07c47f01',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11302/parallel_studio_xe_2017_update2_composer_edition.tgz')
    version('17.0.1',     '1f31976931ed8ec424ac7c3ef56f5e85',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10978/parallel_studio_xe_2017_update1_composer_edition.tgz')
    version('17.0.0',     'b67da0065a17a05f110ed1d15c3c6312',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9656/parallel_studio_xe_2017_composer_edition.tgz')
    version('16.0.4',      '2bc9bfc9be9c1968a6e42efb4378f40e',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9785/parallel_studio_xe_2016_composer_edition_update4.tgz')
    version('16.0.3',     '3208eeabee951fc27579177b593cefe9',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9063/parallel_studio_xe_2016_composer_edition_update3.tgz')
    version('16.0.2',     '1133fb831312eb519f7da897fec223fa',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8680/parallel_studio_xe_2016_composer_edition_update2.tgz')

    variant('rpath', default=True, description="Add rpath to .cfg files")

    def install(self, spec, prefix):
        components = []
        all_components = get_all_components()
        regex = '(comp|openmp|intel-tbb|icc|ifort|psxe|icsxe-pset)'
        components = filter_pick(all_components, re.compile(regex).search)

        self.intel_components = ';'.join(components)
        IntelInstaller.install(self, spec, prefix)

        absbindir = os.path.split(os.path.realpath(os.path.join(
            self.prefix.bin, "icc")))[0]
        abslibdir = os.path.split(os.path.realpath(os.path.join(
            self.prefix.lib, "intel64", "libimf.a")))[0]

        # symlink or copy?
        os.symlink(self.global_license_file,
                   os.path.join(absbindir, "license.lic"))

        if spec.satisfies('+rpath'):
            for compiler_command in ["icc", "icpc", "ifort"]:
                cfgfilename = os.path.join(absbindir, "%s.cfg" %
                                           compiler_command)
                with open(cfgfilename, "w") as f:
                    f.write('-Xlinker -rpath -Xlinker %s\n' % abslibdir)

        os.symlink(os.path.join(self.prefix.man, "common", "man1"),
                   os.path.join(self.prefix.man, "man1"))

    def setup_environment(self, spack_env, run_env):

        # Remove paths that were guessed but are incorrect for this package.
        run_env.remove_path('LIBRARY_PATH',
                            join_path(self.prefix, 'lib'))
        run_env.remove_path('LD_LIBRARY_PATH',
                            join_path(self.prefix, 'lib'))
        run_env.remove_path('CPATH',
                            join_path(self.prefix, 'include'))

        # Add the default set of variables
        run_env.prepend_path('LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'intel64'))
        run_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'intel64'))
        run_env.prepend_path('LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib',
                                       'intel64', 'gcc4.4'))
        run_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib',
                                       'intel64', 'gcc4.4'))
        run_env.prepend_path('CPATH',
                             join_path(self.prefix, 'tbb', 'include'))
        run_env.prepend_path('MIC_LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'mic'))
        run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'mic'))
        run_env.prepend_path('MIC_LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib', 'mic'))
        run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib', 'mic'))
