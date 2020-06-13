# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Pip(Package):
    """Process-in-Process"""

    homepage = "https://github.com/RIKEN-SysSoft/PiP"
    git      = "https://github.com/RIKEN-SysSoft/PiP.git"

    # maintainers = ['github_user1', 'github_user2']

    version('2', branch='pip-2-blt')
    version('1', branch='pip-1')

    # for PiP-gdb
    depends_on('texinfo', type='build')

    #resource(name='PiP-glibc', git='https://github.com/RIKEN-SysSoft/PiP-glibc.git', branch='centos/glibc-2.17-260.el7.pip.branch', destination='PiP-glibc')
    resource(name='PiP-gdb', git='https://github.com/RIKEN-SysSoft/PiP-gdb.git', branch='pip-centos7', destination='PiP-gdb')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check(self):
        make('check') # TODO: replace with 'install-test'

    def install(self, spec, prefix):
        bash = which('bash')

        #glibc_dir = prefix
        #with working_dir('PiP-glibc/PiP-glibc.build', create=True):
        #    bash('../PIP-glibc/build.sh', glibc_dir)

        configure('--prefix=%s' % prefix)
                  #'--with-glibc-libdir=%s/lib' % glibc_dir)
        make()
        make('install')
        bash('%s/bin/piplnlibs' % prefix)

        with working_dir('PiP-gdb/PiP-gdb'):
            bash('build.sh',
                 '--prefix=%s' % prefix,
                 #'--with-glibc-libdir=%s/lib' % glibc_dir,
                 '--with-pip=%s' % prefix)
