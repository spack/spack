# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ProcessInProcess(Package):
    """Process-in-Process"""

    homepage = "https://github.com/RIKEN-SysSoft/PiP"
    git      = "https://github.com/RIKEN-SysSoft/PiP.git"

    version('2', branch='pip-2', preferred=True)
    version('3', branch='pip-3')

    conflicts('%gcc@:3', when='os=centos7')
    conflicts('%gcc@5:', when='os=centos7')
    conflicts('%gcc@:3', when='os=rhel7')
    conflicts('%gcc@5:', when='os=rhel7')
    conflicts('%gcc@:7', when='os=centos8')
    conflicts('%gcc@9:', when='os=centos8')
    conflicts('%gcc@:7', when='os=rhel8')
    conflicts('%gcc@9:', when='os=rhel8')

    # packages required for building PiP-gdb
    depends_on('texinfo', type='build')

    # resources for version 2
    resource(name='PiP-glibc',
             git='https://github.com/RIKEN-SysSoft/PiP-glibc.git',
             branch='centos/glibc-2.17-260.el7.pip.branch',
             destination='PiP-glibc',
             when='@2 os=centos7')
    resource(name='PiP-glibc',
             git='https://github.com/RIKEN-SysSoft/PiP-glibc.git',
             branch='centos/glibc-2.17-260.el7.pip.branch',
             destination='PiP-glibc',
             when='@2 os=rhel7')
    resource(name='PiP-glibc',
             git='https://github.com/RIKEN-SysSoft/PiP-glibc.git',
             branch='centos/glibc-2.28-72.el8_1.1.pip.branch',
             destination='PiP-glibc',
             when='@2 os=centos8')
    resource(name='PiP-glibc',
             git='https://github.com/RIKEN-SysSoft/PiP-glibc.git',
             branch='centos/glibc-2.28-72.el8_1.1.pip.branch',
             destination='PiP-glibc',
             when='@2 os=rhel8')

    resource(name='PiP-gdb',
             git='https://github.com/RIKEN-SysSoft/PiP-gdb.git',
             branch='centos/gdb-7.6.1-94.el7.pip.branch',
             destination='PiP-gdb',
             when='@2 os=centos7')
    resource(name='PiP-gdb',
             git='https://github.com/RIKEN-SysSoft/PiP-gdb.git',
             branch='centos/gdb-7.6.1-94.el7.pip.branch',
             destination='PiP-gdb',
             when='@2 os=rhel7')
    resource(name='PiP-gdb',
             git='https://github.com/RIKEN-SysSoft/PiP-gdb.git',
             branch='centos/gdb-7.6.1-94.el7.pip.branch',
             destination='PiP-gdb',
             when='@2 os=centos8')
    resource(name='PiP-gdb',
             git='https://github.com/RIKEN-SysSoft/PiP-gdb.git',
             branch='centos/gdb-7.6.1-94.el7.pip.branch',
             destination='PiP-gdb',
             when='@2 os=rhel8')

    # resources for version 3
    resource(name='PiP-glibc',
             git='https://github.com/RIKEN-SysSoft/PiP-glibc.git',
             branch='centos/glibc-2.17-260.el7.pip.branch',
             destination='PiP-glibc',
             when='@3 os=centos7')
    resource(name='PiP-glibc',
             git='https://github.com/RIKEN-SysSoft/PiP-glibc.git',
             branch='centos/glibc-2.17-260.el7.pip.branch',
             destination='PiP-glibc',
             when='@3 os=rhel7')
    resource(name='PiP-glibc',
             git='https://github.com/RIKEN-SysSoft/PiP-glibc.git',
             branch='centos/glibc-2.28-72.el8_1.1.pip.branch',
             destination='PiP-glibc',
             when='@3 os=centos8')
    resource(name='PiP-glibc',
             git='https://github.com/RIKEN-SysSoft/PiP-glibc.git',
             branch='centos/glibc-2.28-72.el8_1.1.pip.branch',
             destination='PiP-glibc',
             when='@3 os=rhel8')

    resource(name='PiP-gdb',
             git='https://github.com/RIKEN-SysSoft/PiP-gdb.git',
             branch='centos/gdb-7.6.1-94.el7.pip.branch',
             destination='PiP-gdb',
             when='@3 os=centos7')
    resource(name='PiP-gdb',
             git='https://github.com/RIKEN-SysSoft/PiP-gdb.git',
             branch='centos/gdb-7.6.1-94.el7.pip.branch',
             destination='PiP-gdb',
             when='@3 os=rhel7')
    resource(name='PiP-gdb',
             git='https://github.com/RIKEN-SysSoft/PiP-gdb.git',
             branch='centos/gdb-7.6.1-94.el7.pip.branch',
             destination='PiP-gdb',
             when='@3 os=centos8')
    resource(name='PiP-gdb',
             git='https://github.com/RIKEN-SysSoft/PiP-gdb.git',
             branch='centos/gdb-7.6.1-94.el7.pip.branch',
             destination='PiP-gdb',
             when='@3 os=rhel8')

    # resource for PiP testsuite
    resource(name='PiP-Testsuite',
             git='https://github.com/RIKEN-SysSoft/PiP-Testsuite.git',
             destination='PiP-Testsuite')

    def install(self, spec, prefix):
        "Install Process-in-Process inclduing PiP-glibc, PiP-gdb and PiP-Testsuite"

        # checking os and arch
        arch = self.spec.architecture
        target = self.spec.target
        if arch.os not in ['centos7', 'rhel7', 'centos8', 'rhel8']:
            raise InstallError('PIP is only available for rhel/centos 7 or 8')
        if target.family not in ['x86_64', 'aarch64']:
            raise InstallError('PIP is only available for x86_64 and aarch64')

        bash = which('bash')

        # installing PiP-glibc
        glibc_builddir = join_path('PiP-glibc', 'PiP-glibc.build')
        with working_dir(glibc_builddir, create=True):
            bash(join_path('..', 'PiP-glibc', 'build.sh'), prefix.glibc)
        configure('--prefix=%s' % prefix,
                  '--with-glibc-libdir=%s' % prefix.glibc.lib)

        #  installing PiP lib
        make()
        make('install')
        make('doc')  # installing already-doxygen-ed documents (man pages, html, ...)

        # installing PiP-gdb
        with working_dir(join_path('PiP-gdb', 'PiP-gdb')):
            bash('build.sh', '--prefix=%s' % prefix, '--with-pip=%s' % prefix)

        # running testsuite
        with working_dir(join_path('PiP-Testsuite', 'PiP-Testsuite')):
            bash('configure', '--with-pip=%s' % prefix)
            make()
            make('test')
