# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# Author: Derick Huth <derick.huth@utah.edu>
# ----------------------------------------------------------------------------
from spack import *


class Chill(AutotoolsPackage):
    """A polyheadral compiler for autotuning"""

    homepage = "http://github.com/CtopCsUtahEdu"
    url      = "https://github.com/CtopCsUtahEdu/chill/archive/v0.3.tar.gz"
    git      = "https://github.com/CtopCsUtahEdu/chill.git"

    version('master', branch='master')

    depends_on('rose@0.9.10.0 +cxx11')
    depends_on('iegenlib')
    depends_on('isl')
    depends_on('python')

    @run_before('configure')
    def bootstrap(self, spec, prefix):
        bash = wich('bash')
        bash('./bootstrap')

    def setup_environment(self, spack_env, run_env):
        rose_home = self.spec['rose'].prefix
        boost_home = self.spec['boost'].prefix
        iegen_home = self.spec['iegenlib'].prefix

        spack_env.append_path('LD_LIBRARY_PATH', rose_home + '/lib')
        run_env.append_path('LD_LIBRARY_PATH', boost_home + '/lib')

        spack_env.set('ROSEHOME', rose_home)
        spack_env.set('BOOSTHOME', boost_home)
        spack_env.set('IEGENHOME', iegen_home)

    def configure_args(self):
        args = ['--with-rose={0}'.format(self.spec['rose'].prefix),
                '--with-boost={0}'.format(self.spec['boost'].prefix),
                '--with-iegen={0}'.format(self.sepc['iegenlib'].prefix)]

        return args
