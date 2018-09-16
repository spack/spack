##############################################################################
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

from spack import *


class MofemUsersModules(CMakePackage):
    """MofemUsersModules creates installation environment for user-provided
    modules and extends of mofem-cephas package. The CMakeList.txt file for
    user modules is located in mofem-cephas/user_modules prefix.
    MofemUsersModules itself does not contain any code (is a dummy with a
    single dummy version). It provide sources location of users modules, i.e.
    mofem-fracture-module. Those are kept as a stand-alone package (instead
    of resources) as they have different versions and developers. One can
    install the extension, f.e. spack installs extension spack install
    mofem-fracture-module. Next, create a symlink to run the code, f.e. spack
    view symlink um_view mofem-cephas, and activate the extension, i.e. spack
    activate um_view mofem-minimal-surface-equation. Basic mofem
    functionality is available when with spack install mofem-users-modules,
    it provides simple examples for calculating elasticity problems,
    magnetostatics, saturated and unsaturated flow and a couple more. For
    more information how to work with Spack and MoFEM see
    http://mofem.eng.gla.ac.uk/mofem/html/install_spack.html"""

    homepage = "http://mofem.eng.gla.ac.uk"
    url = "https://bitbucket.org/likask/mofem-joseph/downloads/users_modules_dummy"

    version('0.8.13', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)
    version('0.8.12', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)
    version('0.8.11', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)
    version('0.8.10', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)
    version('0.8.9', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)
    version('0.8.8', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)
    version('0.8.7', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)
    version('develop', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)

    maintainers = ['likask']

    variant('copy_user_modules', default=True,
        description='Copy user modules directory instead linking')

    extends('mofem-cephas')
    depends_on('mofem-cephas@0.8.13', when='@0.8.13')
    depends_on('mofem-cephas@0.8.12', when='@0.8.12')
    depends_on('mofem-cephas@0.8.11', when='@0.8.11')
    depends_on('mofem-cephas@0.8.10', when='@0.8.10')
    depends_on('mofem-cephas@0.8.9', when='@0.8.9')
    depends_on('mofem-cephas@0.8.8', when='@0.8.8')
    depends_on('mofem-cephas@0.8.7', when='@0.8.7')
    depends_on('mofem-cephas@develop', when='@develop')

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        spec = self.spec
        return spec['mofem-cephas'].prefix.users_modules

    def cmake_args(self):
        spec = self.spec

        options = []

        # obligatory options
        options.extend([
            '-DWITH_SPACK=YES',
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO')])

        # build tests
        options.append('-DMOFEM_UM_BUILD_TESTS={0}'.format(
            'ON' if self.run_tests else 'OFF'))

        return options
