# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Helics(CMakePackage):
    """HELICS is a general-purpose, modular, highly-scalable co-simulation
    framework that runs cross-platform (Linux, Windows, and Mac OS X) and
    supports both event driven and time series simulation."""

    homepage = "https://github.com/GMLC-TDC/HELICS"
    url      = "https://github.com/GMLC-TDC/HELICS/releases/download/v2.4.1/Helics-v2.4.1-source.tar.gz"
    git      = "https://github.com/GMLC-TDC/HELICS.git"

    maintainers = ['nightlark']

    version('develop', branch='develop', submodules=True)
    version('master', branch='master', submodules=True)
    version('2.5.0', sha256='6f4f9308ebb59d82d71cf068e0d9d66b6edfa7792d61d54f0a61bf20dd2a7428')
    version('2.4.2', sha256='957856f06ed6d622f05dfe53df7768bba8fe2336d841252f5fac8345070fa5cb')
    version('2.4.1', sha256='ac077e9efe466881ea366721cb31fb37ea0e72a881a717323ba4f3cdda338be4')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('apps', default=True, description="Install the HELICS apps")
    variant('c_shared', default=True, description="Install the C shared library")
    variant('cxx_shared', default=True, description="Install the CXX shared library")
    variant('zmq', default=True, description="Enable ZeroMQ core types")
    variant('tcp', default=True, description="Enable TCP core types")
    variant('udp', default=True, description="Enable UDP core type")
    variant('ipc', default=True, description="Enable IPC core type")
    variant('inproc', default=True, description="Enable in-process core type")
    variant('mpi', default=False, description="Enable MPI core type")
    variant('boost', default=True, description="Compile with Boost libraries")
    variant('asio', default=True, description="Compile with ASIO libraries")
    variant('swig', default=False, description="Build language bindings with SWIG")
    variant('webserver', default=True, description="Enable the integrated webserver in the HELICS broker server")
    variant('python', default=False, description="Enable Python interface")

    # Build dependency
    depends_on('git', type='build', when='@master:')
    depends_on('cmake@3.4:', type='build')
    depends_on('boost@1.70:', type='build', when='+boost')
    depends_on('swig@3.0:', type='build', when='+swig')

    depends_on('libzmq@4.3:', when='+zmq')
    depends_on('mpi@2', when='+mpi')
    depends_on('python@3:', when='+python')

    # OpenMPI doesn't work with HELICS <=2.4.1
    conflicts('^openmpi', when='@:2.4.1 +mpi')

    # Boost is required for ipc and webserver options
    conflicts('+ipc', when='~boost')
    conflicts('+webserver', when='~boost')

    # ASIO (vendored in HELICS repo) is required for tcp and udp options
    conflicts('+tcp', when='~asio')
    conflicts('+udp', when='~asio')

    extends('python', when='+python')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DHELICS_BUILD_EXAMPLES=OFF',
            '-DHELICS_BUILD_TESTS=OFF',
        ]

        # HELICS core type CMake options
        args.append('-DENABLE_ZMQ_CORE={0}'.format(
            'ON' if '+zmq' in spec else 'OFF'))
        args.append('-DENABLE_TCP_CORE={0}'.format(
            'ON' if '+tcp' in spec else 'OFF'))
        args.append('-DENABLE_UDP_CORE={0}'.format(
            'ON' if '+udp' in spec else 'OFF'))
        args.append('-DENABLE_IPC_CORE={0}'.format(
            'ON' if '+ipc' in spec else 'OFF'))
        args.append('-DENABLE_INPROC_CORE={0}'.format(
            'ON' if '+inproc' in spec else 'OFF'))
        args.append('-DENABLE_MPI_CORE={0}'.format(
            'ON' if '+mpi' in spec else 'OFF'))

        # HELICS shared library options
        args.append('-DHELICS_DISABLE_C_SHARED_LIB={0}'.format(
            'OFF' if '+c_shared' in spec else 'ON'))
        args.append('-DHELICS_BUILD_CXX_SHARED_LIB={0}'.format(
            'ON' if '+cxx_shared' in spec else 'OFF'))

        # HELICS executable app options
        args.append('-DHELICS_BUILD_APP_EXECUTABLES={0}'.format(
            'ON' if '+apps' in spec else 'OFF'))
        args.append('-DHELICS_DISABLE_WEBSERVER={0}'.format(
            'OFF' if '+webserver' in spec else 'ON'))

        # Extra HELICS library dependencies
        args.append('-DHELICS_DISABLE_BOOST={0}'.format(
            'OFF' if '+boost' in spec else 'ON'))
        args.append('-DHELICS_DISABLE_ASIO={0}'.format(
            'OFF' if '+asio' in spec else 'ON'))

        # SWIG
        args.append('-DHELICS_ENABLE_SWIG={0}'.format(
            'ON' if '+swig' in spec else 'OFF'))

        # Python
        args.append('-DBUILD_PYTHON_INTERFACE={0}'.format(
            'ON' if '+python' in spec else 'OFF'))

        return args

    def setup_run_environment(self, env):
        spec = self.spec
        if '+python' in spec:
            env.prepend_path('PYTHONPATH', self.prefix.python)
