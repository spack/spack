# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Must(CMakePackage):
    """MPI Runtime Correctness Analysis
    MUST detects usage errors of the Message Passing Interface (MPI) and reports them to the user. As
    MPI calls are complex and usage errors common, this functionality is extremely helpful for application
    developers that want to develop correct MPI applications. This includes errors that already manifest –
    segmentation faults or incorrect results – as well as many errors that are not visible to the application
    developer or do not manifest on a certain system or MPI implementation.
    """

    homepage = "https://itc.rwth-aachen.de/must/"
    url      = "https://hpc.rwth-aachen.de/must/files/MUST-v1.7.2.tar.gz"

    version('1.7.2', sha256='616c54b7487923959df126ac4b47ae8c611717d679fe7ec29f57a89bf0e2e0d0')
    version('1.7.1', sha256='de3f6144a433035d24952c1acdf1acac47bcd843b24243bd8c0467a0567b1ed6')
    version('1.7', sha256='23c3a41d7dfe050bc9bc64ce8e0aa47970bb7747262c681f4977f72a6657c591')
    version('1.6', sha256='920956a85e4749299b2c6872e47ee872d67f09037b3fd084028d02d922b01fe4')

    # build variants
    variant('fortran', default=True,
            description='Build MUST with Fortran support.')
    variant('callpath', default=False,
            description='Enable stacktraces with the stackwalker from dyninst.')
    variant('backward', default=True,
            description='Enable stacktraces with backward-cpp.')
    variant('graphviz', default=False,
            description='Automatically call graphviz dot tool to visualize deadlocks.')
    variant('tests', default=False,
            description='Selects whether tests are built.')


    # required dependencies
    depends_on('cmake@3.9:', type='build')
    depends_on('python@2.6:2.7', type='build')
    depends_on('awk', type='build')
    # not sure if those are required too for building...
    # depends_on('binutils')
    # depends_on('help2man')
    # depends_on('doxygen')
    depends_on('libxml2')
    depends_on('mpi')
    # also depends on GTI and PnMPI but provides internal versions of those since 1.6

    # optional dependencies
    depends_on('dyninst', when='+callpath')
    depends_on('graphviz', when='+graphviz')

    # to speed up the tool preparation time,
    # must provides some prebuilt configurations for typical usage.
    # So install those, too
    install_targets = ['install', 'install-prebuilds']


    @run_before('cmake')
    def check_fortran(self):
        is_no_fortran_compiler = not self.compiler.f77 and not self.compiler.fc
        if self.spec.satisfies('+fortran'):
            if is_no_fortran_compiler:
                raise InstallError('must+fortran requires Fortran compiler '
                                   'but no Fortran compiler found!')

    def cmake_args(self):
        args = []
        spec = self.spec
        on_off = {True: 'ON', False: 'OFF'}

        has_fortran = spec.satisfies('+fortran')
        has_tests = spec.satisfies('+tests')
        has_backward = spec.satisfies('+backward')
        has_callpath = spec.satisfies('+callpath')

        args.append('-DENABLE_FORTRAN:BOOL={0}'.format(on_off[has_fortran]))
        args.append('-DENABLE_TESTS:BOOL={0}'.format(on_off[has_tests]))
        args.append('-DUSE_BACKWARD:BOOL={0}'.format(on_off[has_backward]))
        args.append('-DUSE_CALLPATH:BOOL={0}'.format(on_off[has_callpath]))
        if has_callpath:
            args.append('-DCALLPATH_STACKWALKER_EXTRA_LIBRARIES:STRING="stackwalk"')
            #args.append('-DCALLPATH_STACKWALKER_EXTRA_LIBRARIES:STRING="{0}/lib/libstackwalker.so"'.format(spec['dyninst'].prefix))
        
        # we need to specify the real compilers
        # WARNING: "-DMUST_C_COMPILER:STRING:STRING=..." does not overwrite internal variables - "-DMUST_C_COMPILER=..." (without :STRING) seems to work.
        args.append('-DMUST_C_COMPILER={0}'.format(self.compiler.cc))
        args.append('-DMUST_CXX_COMPILER={0}'.format(self.compiler.cxx))
        if spec.satisfies('+fortran'):
            args.append('-DMUST_Fortran_COMPILER={0}'.format(self.compiler.fc))

        return args
