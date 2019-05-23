##############################################################################
# Copyright (c) 2013-2019, Lawrence Livermore National Security, LLC.
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
# ----------------------------------------------------------------------------
# Author: Derick Huth <derick.huth@utah.edu>
# ----------------------------------------------------------------------------
from spack import *


class Chill(Package):
    """A polyheadral compiler for autotuning"""

    homepage = "http://github.com/CtopCsUtahEdu"
    url      = "https://github.com/CtopCsUtahEdu/chill/archive/v0.3.tar.gz"
    git      = "https://github.com/CtopCsUtahEdu/chill.git"

    version('master', branch='master')

    depends_on('rose-for-chill@0.9.10.0 +cxx11')
    depends_on('iegenlib')
    depends_on('isl')
    depends_on('python')

    def setup_environment(self, spack_env, run_env):
        rose_home = self.spec['rose-for-chill'].prefix
        boost_home = self.spec['boost'].prefix
        iegen_home = self.spec['iegenlib'].prefix

        spack_env.append_path('LD_LIBRARY_PATH', rose_home + '/lib')
        run_env.append_path('LD_LIBRARY_PATH', boost_home + '/lib')

        spack_env.set('ROSEHOME', rose_home)
        spack_env.set('BOOSTHOME', boost_home)
        spack_env.set('IEGENHOME', iegen_home)
    
    def install(self, spec, prefix):
        bash = which('bash')
        bash('./bootstrap')
        
        configure(
            '--prefix={0}'.format(prefix),
            '--with-rose={0}'.format(spec['rose'].prefix),
            '--with-boost={0}'.format(spec['boost'].prefix),
            '--with-iegen={0}'.format(spec['iegenlib'].prefix))
        make()
        make('install')
