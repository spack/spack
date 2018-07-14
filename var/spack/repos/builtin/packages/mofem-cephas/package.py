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


class MofemCephas(CMakePackage):
    """mofem-cephas core library"""

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return 'mofem'

    homepage = "http://mofem.eng.gla.ac.uk"
    url = "https://bitbucket.org/likask/mofem-cephas.git"

    maintainers = ['likask']

    version('0.8.3', git='https://bitbucket.org/likask/mofem-cephas.git',
        tag='v0.8.3', submodules=True)
    version('develop',
        git='https://bitbucket.org/likask/mofem-cephas.git',
        branch='develop')

    # This option can be only used for development of core lib
    variant('copy_user_modules', default=True,
        description='Copy user modules directory instead linking to source')
    variant('adol-c', default=True, description='Compile with Adol-C')
    variant('tetgen', default=True, description='Compile with Tetgen')
    variant('med', default=True, description='Compile with Med')
    variant('slepc', default=True, description='Compile with Slepc')
    variant('doxygen', default=False, description='Install doxygen')

    conflicts('+adol-c', when='+with_adol-c')
    conflicts('+tetgen', when='+with_tetgen')
    conflicts('+med', when='+with_med')

    depends_on("mpi")
    depends_on("parmetis")
    # Fixed version of hdf5, to remove some problems with dependent
    # packages, f.e. MED format
    depends_on("hdf5@:1.8.19+hl+mpi")
    depends_on("petsc@:3.9.2+mumps+mpi")
    depends_on('slepc', when='+slepc')
    depends_on("moab")
    # Upper bound set to ADOL-C until issues with memory leaks
    # for versions 2.6: fully resolved
    depends_on("adol-c@2.5.2~examples", when="+adol-c")
    depends_on("tetgen", when="+tetgen")
    depends_on("med", when='+med')
    depends_on('doxygen+graphviz', when='+doxygen')
    depends_on('graphviz', when='+doxygen')

    extendable = True

    def cmake_args(self):
        spec = self.spec
        options = []

        # obligatory options
        options.extend([
            '-DWITH_SPACK=1',
            '-DPETSC_DIR=%s' % spec['petsc'].prefix,
            '-DPETSC_ARCH=',
            '-DMOAB_DIR=%s' % spec['moab'].prefix])

        # variant packages
        if '+adol-c' in spec:
            options.extend(['-DADOL-C_DIR=%s' % spec['adol-c'].prefix])

        if '+tetgen' in spec:
            options.extend(['-DTETGEN_DIR=%s' % spec['tetgen'].prefix])

        if '+med' in spec:
            options.extend(['-DMED_DIR=%s' % spec['med'].prefix])

        if '+slepc' in spec:
            options.extend(['-DSLEPC_DIR=%s' % spec['slepc'].prefix])

        # copy users modules, i.e. stand alone vs linked users modules
        options.extend([
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO')])
        return options
