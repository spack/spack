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

class MofemCephas(CMakePackage):
    """mofem-cephas core library"""

    extendable = True

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return os.path.join(self.stage.source_path, 'mofem')

    homepage = "http://mofem.eng.gla.ac.uk"
    url = "https://likask@bitbucket.org/likask/mofem-cephas.git"

    version('0.7.29', git='https://likask@bitbucket.org/likask/mofem-cephas.git', tag='v0.7.29')
    version('0.7.28', git='https://likask@bitbucket.org/likask/mofem-cephas.git', tag='v0.7.28')
    version('0.7.27', git='https://likask@bitbucket.org/likask/mofem-cephas.git', tag='v0.7.27')
    version('develop', git='https://likask@bitbucket.org/likask/mofem-cephas.git', branch='develop')

    variant('with_adol_c', default=True,
            description='Install ADOL-C with MoFEM')
    variant('with_tetgen', default=True,
            description='Install TetGen with MoFEM')
    variant('with_med', default=True,
            description='Install MED with MoFEM')
    variant('copy_user_modules', default=True,
	    description='Copy user modules directory instead if making ling to source')
    variant('slepc', default=False, description='Compile with Slepc')
    variant('doxygen', default=False, description='Install doxygen')

    depends_on("openmpi") 
    depends_on("parmetis") 
    depends_on("hdf5@1.8.19 hl=True") 
    depends_on("petsc@3.9.2 ^hdf5@1.8.19 mumps=True")
    depends_on("moab@5.0.0 ^hdf5@1.8.19")
    depends_on("cmake")
    depends_on('doxygen+graphviz', when='+doxygen')
    depends_on('graphviz', when='+doxygen')
    depends_on('slepc', when='+slepc')

    def cmake_args(self):
        spec = self.spec
        options = []

        """ obligatory options """
        options.extend([
            '-DWITH_SPACK=1',
            '-DPETSC_DIR=%s' % spec['petsc'].prefix,
            '-DPETSC_ARCH=',  
            '-DMOAB_DIR=%s' % spec['moab'].prefix])

        """ mofem extensions compiled with mofem """
        options.extend([
            '-DWITH_ADOL-C=%s' % ('YES' if '+with_adol_c' in spec else 'NO'),
            '-DWITH_TETGEN=%s' % ('YES' if '+with_tetgen' in spec else 'NO'),
            '-DWITH_MED=%s' % ('YES' if '+with_med' in spec else 'NO')]
        )

        """ variant packages """
        if '+slepc' in spec:
                options.extend(['-DSLEPC_DIR=%s' % spec['slepc'].prefix])

        """ copy users modules, i.e. stand alone vs linked users modules"""
        options.extend([
               '-DSTAND_ALLONE_USERS_MODULES=%s' % ('YES' if '+copy_user_modules' in spec else 'NO') 
        ])
        
        return options


