#############################################################################
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


class Chapel(AutotoolsPackage):
    """Chapel is a modern programming language that is:
    parallel: contains first-class concepts for concurrent and parallel computation,
    productive: designed with programmability and performance in mind,
    portable: runs on laptops, clusters, the cloud, and HPC systems,
    scalable: supports locality-oriented features for distributed memory systems,
    open-source: hosted on GitHub, permissively licensed"""

    homepage = "https://chapel-lang.org/"
    url      = "https://github.com/chapel-lang/chapel/releases/download/1.18.0/chapel-1.18.0.tar.gz"

    version('1.18.0', sha256='68471e1f398b074edcc28cae0be26a481078adc3edea4df663f01c6bd3b6ae0d')

    depends_on('tcsh', type='build')
    depends_on('perl', type='build')
    depends_on('python', type='build')
    depends_on('m4', type='build')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('MANPATH', join_path(prefix, 'man'))
