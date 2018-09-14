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

    homepage = "http://mofem.eng.gla.ac.uk"
    git      = "https://bitbucket.org/likask/mofem-cephas.git"

    maintainers = ['likask']

    version('develop', branch='develop', submodules=True)
    version('0.8.7', tag='v0.8.7', submodules=True)

    # This option can be only used for development of core lib
    variant('copy_user_modules', default=True,
        description='Copy user modules directory instead linking to source')
    variant('adol-c', default=True, description='Compile with Adol-C')
    variant('tetgen', default=True, description='Compile with Tetgen')
    variant('med', default=True, description='Compile with Med')
    variant('slepc', default=False, description='Compile with Slepc')

    depends_on("mpi")
    depends_on("boost")
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

    extendable = True

    root_cmakelists_dir = 'mofem'

    def cmake_args(self):
        spec = self.spec
        options = []

        # obligatory options
        options.extend([
            '-DWITH_SPACK=YES',
            '-DPETSC_DIR=%s' % spec['petsc'].prefix,
            '-DPETSC_ARCH=',
            '-DMOAB_DIR=%s' % spec['moab'].prefix,
            '-DBOOST_DIR=%s' % spec['boost'].prefix])

        # build tests
        options.append('-DMOFEM_BUILD_TETS={0}'.format(
            'ON' if self.run_tests else 'OFF'))

        # variant packages
        if '+adol-c' in spec:
            options.append('-DADOL-C_DIR=%s' % spec['adol-c'].prefix)

        if '+tetgen' in spec:
            options.append('-DTETGEN_DIR=%s' % spec['tetgen'].prefix)

        if '+med' in spec:
            options.append('-DMED_DIR=%s' % spec['med'].prefix)

        if '+slepc' in spec:
            options.append('-DSLEPC_DIR=%s' % spec['slepc'].prefix)

        # copy users modules, i.e. stand alone vs linked users modules
        options.append(
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO'))
        return options
