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
import os


class MofemUsersModules(CMakePackage):
    """MofemUsersModules collects all user-provided modules and extends
    mofem-cephas package. The CMakeList.txt file for user modules is located
    in mofem-cephas/user_modules prefix. MofemUsersModules itself does not
    contain any code (is a dummy with a single dummy version). We build in
    the self.prefix/build and provide sources location of user modules, i.e.
    mofem-fracture-module. Those are kept as a stand-alone package (instead
    of resources) as they have different versions and developers. For more
    information how to work with Spack and MoFEM see
    http://mofem.eng.gla.ac.uk/mofem/html/install_spack.html"""

    homepage = "http://mofem.eng.gla.ac.uk"
    url = "https://bitbucket.org/likask/mofem-joseph/downloads/users_modules_dummy"
    version('1.0', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)

    maintainers = ['likask']

    variant('copy_user_modules', default=True,
        description='Copy user modules directory instead linking')
    variant('with_metaio', default=False,
        description='Install MetaIO with MoFEM users modules')

    variant('mofem_fracture_module', default=False,
        description="Install fracture mechanics module")
    variant('mofem_minimal_surface_equation', default=False,
        description="Install minimal surface equation module")

    extends('mofem-cephas')

    depends_on("mofem-fracture-module", type=('build', 'link', 'run'),
        when='+mofem_fracture_module')
    depends_on("mofem-minimal-surface-equation", type=('build', 'link', 'run'),
        when='+mofem_minimal_surface_equation')

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        spec = self.spec
        return os.path.join(spec['mofem-cephas'].prefix.users_modules)

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        return os.path.join(self.prefix, 'build')

    def cmake_args(self):
        spec = self.spec

        options = []

        # obligatory options
        options.extend([
            '-DWITH_METAIO=%s' % ('YES' if '+with_metaio' in spec else 'NO'),
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO')])

        ext_um_modules_opt = '-DEXTERNAL_MODULE_SOURCE_DIRS='
        if '+mofem_fracture_module' in spec:
            ext_um_modules_opt += '%s;' % \
                spec['mofem-fracture-module'].prefix.ext_users_modules

        if '+mofem_minimal_surface_equation' in spec:
            ext_um_modules_opt += '%s;' % \
                spec['mofem-minimal-surface-equation'].prefix.ext_users_modules

        options.append(ext_um_modules_opt)

        return options

    phases = ['cmake', 'build']
