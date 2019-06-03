# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Brayns(CMakePackage):
    """Visualizer for large-scale and interactive ray-tracing of neurons"""

    homepage = "https://github.com/BlueBrain/Brayns"
    git = "https://github.com/BlueBrain/Brayns.git"
    generator = 'Ninja'

    version('develop', submodules=True)
    version('0.8.0', tag='0.8.0', submodules=True, preferred=True)

    variant('assimp', default=True, description='Build with assimp support')
    variant('ospray', default=True, description='Enable OSPRray engine')
    variant('deflect', default=True, description='Enable Deflect support')
    variant('brion', default=False, description='Build CircuitViewer support')
    variant('net', default=True, description='Enable web interface')
    variant('opendeck', default=False, description='Enable OpenDeck support')
    variant('viewer', default=True, description='Build braynsViewer app')
    variant('optix', default=False, description='Build Optix engine')

    depends_on('cmake@3.1:', type='build')
    depends_on('ispc', type='build')
    depends_on('ninja', type='build')

    depends_on('assimp', when='+assimp')
    depends_on('brion', when='+brion')
    depends_on('deflect ~deflect-qt', when='+deflect')
    depends_on('freeimage')
    depends_on('glew', when='+viewer')
    depends_on('libjpeg-turbo', when='+net')
    depends_on('libuv', when='+net')
    depends_on('opengl', when='+viewer')
    depends_on('ospray', when='+ospray')
    depends_on('rockets', when='+net')
    depends_on('vrpn', when='+opendeck')
    depends_on('optix@5.0.1', when='+optix')
    depends_on('cuda', when='+optix')

    def cmake_args(self):
        args = ['-DDISABLE_SUBPROJECTS=ON']
        if '+opendeck' in self.spec:
            args.append('-DBRAYNS_OPENDECK_ENABLED=ON')
            args.append('-DBRAYNS_VRPN_ENABLED=ON')
        if '+brion' in self.spec:
            args.append('-DBRAYNS_CIRCUITVIEWER_ENABLED=ON')
        if '+net' in self.spec:
            args.append('-DBRAYNS_NETWORKING_ENABLED=ON')
        if '+deflect' in self.spec:
            args.append('-DBRAYNS_DEFLECT_ENABLED=ON')
        if '+optix' in self.spec:
            args.append('-DBRAYNS_OPTIX_ENABLED=ON')
            args.append('-DBRAYNS_OPTIX_TESTS_ENABLED=ON')
        return args
