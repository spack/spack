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


class Ants(CMakePackage):
    """ANTs extracts information from complex datasets that include imaging.
       Paired with ANTsR (answer), ANTs is useful for managing, interpreting
       and visualizing multidimensional data. ANTs is popularly considered a
       state-of-the-art medical image registration and segmentation toolkit.
       ANTs depends on the Insight ToolKit (ITK), a widely used medical image
       processing library to which ANTs developers contribute.
    """

    homepage = "http://stnava.github.io/ANTs/"
    url      = "https://github.com/ANTsX/ANTs/archive/v2.2.0.tar.gz"

    version('2.2.0', '5661b949268100ac0f7baf6d2702b4dd')

    def install(self, spec, prefix):
        with working_dir(join_path('spack-build', 'ANTS-build'), create=False):
            make("install")
        install_tree('Scripts', prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.set('ANTSPATH', self.prefix.bin)
