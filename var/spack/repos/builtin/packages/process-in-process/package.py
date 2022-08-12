# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ProcessInProcess(Package):
    """Process-in-Process"""

    enable_pip_v3  = False
    enable_pip_gdb = False
    # we cannot install PiP-gdb (PiP-aware GDB)
    # since the ncureses package cannot be installed by using Spack
    # --> https://github.com/spack/spack/issues/8675

    homepage = "https://github.com/procinproc/procinproc.github.io"
    git      = "https://github.com/procinproc/PiP.git"

    maintainers = ['ahori']

    conflicts('platform=darwin',  msg='Darwin is not supported.')
    conflicts('platform=windows', msg='Windows is not supported.')

    # PiP version 1 is obsolete
    version('2', branch='pip-2', preferred=True)
    if enable_pip_v3:
        version('3', branch='pip-3')  # experimental

    conflicts('%gcc@:3', when='os=centos7')
    conflicts('%gcc@5:', when='os=centos7')
    conflicts('%gcc@:3', when='os=rhel7')
    conflicts('%gcc@5:', when='os=rhel7')
    conflicts('%gcc@:7', when='os=centos8')
    conflicts('%gcc@9:', when='os=centos8')
    conflicts('%gcc@:7', when='os=rhel8')
    conflicts('%gcc@9:', when='os=rhel8')

    # packages required for building PiP-glibc
    #    currently none

    # packages required for building PiP-gdb
    if enable_pip_gdb:
        depends_on('texinfo')
        depends_on('ncurses')
        depends_on('systemtap')
        depends_on('libxml2')
        depends_on('pigz')

    # resources for PiP version 2
    #  PiP-glibc resource
    #   for rhel/centos 7
    resource(name='PiP-glibc',
             git='https://github.com/procinproc/PiP-glibc.git',
             branch='centos/glibc-2.17-260.el7.pip.branch',
             destination='PiP-glibc',
             when='@2 os=centos7')
    resource(name='PiP-glibc',
             git='https://github.com/procinproc/PiP-glibc.git',
             branch='centos/glibc-2.17-260.el7.pip.branch',
             destination='PiP-glibc',
             when='@2 os=rhel7')
    #   for rhel/centos 8
    resource(name='PiP-glibc',
             git='https://github.com/procinproc/PiP-glibc.git',
             branch='centos/glibc-2.28-72.el8_1.1.pip.branch',
             destination='PiP-glibc',
             when='@2 os=centos8')
    resource(name='PiP-glibc',
             git='https://github.com/procinproc/PiP-glibc.git',
             branch='centos/glibc-2.28-72.el8_1.1.pip.branch',
             destination='PiP-glibc',
             when='@2 os=rhel8')

    if enable_pip_gdb:
        #  PiP-gdb resource
        #   for rhel/centos 7
        resource(name='PiP-gdb',
                 git='https://github.com/procinproc/PiP-gdb.git',
                 branch='centos/gdb-7.6.1-94.el7.pip.branch',
                 destination='PiP-gdb',
                 when='@2 os=centos7')
        resource(name='PiP-gdb',
                 git='https://github.com/procinproc/PiP-gdb.git',
                 branch='centos/gdb-7.6.1-94.el7.pip.branch',
                 destination='PiP-gdb',
                 when='@2 os=rhel7')
        #   for rhel/centos 8
        resource(name='PiP-gdb',
                 git='https://github.com/procinproc/PiP-gdb.git',
                 branch='centos/gdb-8.2-12.el8.pip.branch',
                 destination='PiP-gdb',
                 when='@2 os=centos8')
        resource(name='PiP-gdb',
                 git='https://github.com/procinproc/PiP-gdb.git',
                 branch='centos/gdb-8.2-12.el8.pip.branch',
                 destination='PiP-gdb',
                 when='@2 os=rhel8')

    if enable_pip_v3:
        # resources for PiP version 3
        #  PiP-glibc resource
        #   for rhel/centos 7
        resource(name='PiP-glibc',
                 git='https://github.com/procinproc/PiP-glibc.git',
                 branch='centos/glibc-2.17-260.el7.pip.branch',
                 destination='PiP-glibc',
                 when='@3 os=centos7')
        resource(name='PiP-glibc',
                 git='https://github.com/procinproc/PiP-glibc.git',
                 branch='centos/glibc-2.17-260.el7.pip.branch',
                 destination='PiP-glibc',
                 when='@3 os=rhel7')
        #   for rhel/centos 8
        resource(name='PiP-glibc',
                 git='https://github.com/procinproc/PiP-glibc.git',
                 branch='centos/glibc-2.28-72.el8_1.1.pip.branch',
                 destination='PiP-glibc',
                 when='@3 os=centos8')
        resource(name='PiP-glibc',
                 git='https://github.com/procinproc/PiP-glibc.git',
                 branch='centos/glibc-2.28-72.el8_1.1.pip.branch',
                 destination='PiP-glibc',
                 when='@3 os=rhel8')

        if enable_pip_gdb:
            #  PiP-gdb resource
            #   for rhel/centos 7
            resource(name='PiP-gdb',
                     git='https://github.com/procinproc/PiP-gdb.git',
                     branch='centos/gdb-7.6.1-94.el7.pip.branch',
                     destination='PiP-gdb',
                     when='@3 os=centos7')
            resource(name='PiP-gdb',
                     git='https://github.com/procinproc/PiP-gdb.git',
                     branch='centos/gdb-7.6.1-94.el7.pip.branch',
                     destination='PiP-gdb',
                     when='@3 os=rhel7')
            #   for rhel/centos 8
            resource(name='PiP-gdb',
                     git='https://github.com/procinproc/PiP-gdb.git',
                     branch='centos/gdb-8.2-12.el8.pip.branch',
                     destination='PiP-gdb',
                     when='@3 os=centos8')
            resource(name='PiP-gdb',
                     git='https://github.com/procinproc/PiP-gdb.git',
                     branch='centos/gdb-8.2-12.el8.pip.branch',
                     destination='PiP-gdb',
                     when='@3 os=rhel8')

    # PiP testsuite (agnostic with PiP and OS versions)
    resource(name='PiP-Testsuite',
             git='https://github.com/procinproc/PiP-Testsuite.git',
             destination='PiP-Testsuite')

    def install(self, spec, prefix):
        "Install Process-in-Process including PiP-glibc (, PiP-gdb)"

        # checking os and arch
        arch   = self.spec.architecture
        target = self.spec.target
        if arch.os not in ['centos7', 'rhel7', 'centos8', 'rhel8']:
            raise InstallError('PiP only supports rhel/centos 7 and 8')
        if target.family not in ['x86_64', 'aarch64']:
            raise InstallError('PiP only supports x86_64 and aarch64')

        bash = which('bash')

        # installing PiP-glibc
        glibc_builddir = join_path('PiP-glibc', 'PiP-glibc.build')
        with working_dir(glibc_builddir, create=True):
            # build.sh does build and install
            bash(join_path('..', 'PiP-glibc', 'build.sh'), prefix.glibc)

        #  installing PiP lib
        configure('--prefix=%s' % prefix,
                  '--with-glibc-libdir=%s' % prefix.glibc.lib)
        make()
        make('install')
        # installing already-doxygen-ed documents (man pages, html, ...)
        make('doc')

        if ProcessInProcess.enable_pip_gdb:
            # installing PiP-gdb
            with working_dir(join_path('PiP-gdb', 'PiP-gdb')):
                # build.sh does build and install
                bash('build.sh', '--prefix=%s' % prefix, '--with-pip=%s' % prefix)
                # testing PiP-gdb
                bash('test.sh', parallel=False)

        # testing PiP by using PiP-Testsuite (another repo), no need install
        with working_dir(join_path('PiP-Testsuite', 'PiP-Testsuite')):
            bash('configure', '--with-pip=%s' % prefix)
            # make test programs
            make()
            # and run the test programs
            make('test10', parallel=False)

# all done !!
