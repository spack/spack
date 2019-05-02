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
#-----------------------------------------------------------------------------
# Author: Derick Huth <derick.huth@utah.edu>
#-----------------------------------------------------------------------------
from spack import *


class Chill(Package):
    """FIXME: Put a proper description of your package here."""
    rose_git        = "https://github.com/rose-compiler/rose-develop.git"
    rose_version    = "v0.9.10.0"
    
    homepage    = "http://github.com/CtopCsUtahEdu"
    url         = "https://github.com/CtopCsUtahEdu/chill/archive/v0.3.tar.gz"
    git         = "https://github.com/CtopCsUtahEdu/chill.git"

    #version('0.3', sha256='574b622368a6bfaadbe9c1fa02fabefdc6c006069246f67d299f943b7e1d8aa3')
    version('master', branch='master')

    depends_on("autoconf@2.69:", type='build')
    depends_on("automake@1.14:", type='build')
    depends_on("libtool@2.4:", type='build')
    depends_on("bison", type='build')
    depends_on("flex", type='build')
    depends_on("boost@1.60.0:1.69.0")
    depends_on('iegenlib')
    depends_on('isl')
    depends_on('python')
    
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        
        with working_dir(self.stage.source_path + '/..'):
            bash('git clone -b {0} {1}'.format(rose_version, rose_git, 'rose_src')
            with working_dir('rose_src'):
                bash('build')
    
    def setup_environment(self, spack_env, run_env):
        boost_home = self.spec['boost'].prefix
        iegen_home = self.spec['iegenlib'].prefix
        
        spack_env.append_path('LD_LIBRARY_PATH', rose_home + '/lib')
        run_env.append_path('LD_LIBRARY_PATH', boost_home + '/lib')
        
        spack_env.set('ROSEHOME', rose_home)
        spack_env.set('BOOSTHOME', boost_home)
        spack_env.set('IEGENHOME', iegen_home)
    
    def install(self, spec, prefix):
        bash = which('bash')
        
        #build rose
        with working_dir(self.stage.build_path + '/..'):
            bash('mkdir rose_build')
            with working_dir('rose_build'):
                bash(self.stage.source_path + '/../rose_src/confgiure'
                    '--prefix={0}'.format(prefix),
                    '--disable-boost-version-check',
                    '--enable-edg_version=4.12',
                    '--with-alternate_backend_C_compiler={0}'.format(self.compiler.cc),
                    '--with-alternate_backend_Cxx_compiler={0}'.format(self.compiler.cxx),
                    '--enable-languages=c,c++',
                    '--disable-tests-directory',
                    '--enable-tutorial-directory={0}'.format('no'),
                    '--without-java',
                    'CXXFLAGS=-std=c++11')
                bash('make install-core')
        
        #build chill
        bash('./bootstrap')
        configure(
            '--prefix={0}'.format(prefix),
            '--with-rose={0}'.format(spec['rose'].prefix),
            '--with-boost={0}'.format(spec['boost'].prefix),
            '--with-iegen={0}'.format(spec['iegenlib'].prefix))
        make()
        make('install')

