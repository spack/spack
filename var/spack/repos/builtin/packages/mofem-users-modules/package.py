##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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

from spack import *
import os
from distutils.dir_util import copy_tree 

class MofemUsersModules(CMakePackage):
    """mofem users modules"""

    homepage = "http://mofem.eng.gla.ac.uk"
    version('1.0', '5a8b22c9cdcad7bbad92b1590d55edb1', expand=False)
    url = "https://bitbucket.org/likask/mofem-joseph/downloads/users_modules_dummy"

    depends_on("mofem-cephas")
    extends('mofem-cephas')

    variant('copy_user_modules', default=True,
	    description='Copy user modules directory insetad if making ling to source')
    variant('with_metaio', default=False,
            description='Install MetaIO with MoFEM users modules')


    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        spec = self.spec
        return os.path.join(spec['mofem-cephas'].prefix, 'users_modules')

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        spec = self.spec
        return spec['mofem-cephas'].prefix


    def cmake_args(self):
        spec = self.spec
        return [
	    '-DWITH_METAIO=%s' % ('YES' if '+with_metaio' in spec else 'NO'),
	    '-DSTAND_ALLONE_USERS_MODULES=%s' % ('YES' if '+copy_user_modules' in spec else 'NO')]

    phases = ['cmake', 'build']

       
