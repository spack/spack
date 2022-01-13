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
    version('0.8.0', tag='0.8.0', submodules=True)
    version('1.0.1', tag='1.0.1', submodules=True)
    version('1.1.0', tag='1.1.0', submodules=True)
    version('2.0.0', tag='2.0.0', submodules=False)
    version('immersive', branch='videostreaming', submodules=True)

    variant('assimp', default=True, description='Build with assimp support')
    variant('ospray', default=True, description='Enable OSPRray engine')
    variant('deflect', default=True, description='Enable Deflect support')
    variant('brion', default=False, description='Build CircuitViewer support')
    variant('net', default=True, description='Enable web interface')
    variant('opendeck', default=False, description='Enable OpenDeck support')
    variant('viewer', default=True, description='Build braynsViewer app')
    variant('optix', default=False, description='Build Optix engine')
    variant('test', default=False, description='Enable extra tests')
    variant('doc', default=False, description='Build documentation')

    depends_on('cmake@3.1:', type='build')
    depends_on('doxygen', type='build', when='+doc')
    depends_on('graphviz', type='build', when='+doc')
    depends_on('ispc', type='build')
    depends_on('ninja', type='build')

    depends_on('assimp@5.0.1', when='@1.1.1: +assimp')
    depends_on('brion', when='+brion')
    depends_on('ffmpeg@4.2.2', when='+net')
    depends_on('git', when='@1.1.1:')
    depends_on('glew', when='+viewer')
    depends_on('glm')
    depends_on('libsonata', when='@1.1.1: +brion')
    depends_on('morphio', when='@1.1.1: +brion')
    depends_on('mvdtool', when='@1.1.1: +brion')
    depends_on('opengl', when='+viewer')
    depends_on('ospray', when='+ospray')
    depends_on('spdlog')

    depends_on('deflect ~deflect-qt', when='@:1.1.0 +deflect')
    depends_on('assimp@4.1.0', when='@:1.1.0 +assimp')
    depends_on('freeimage', when='@:1.1.0')
    depends_on('libarchive', when='@:1.1.0')
    depends_on('cgal', when='@:1.1.0')
    depends_on('libjpeg-turbo', when='@:1.1.0 +net')
    depends_on('libuv', when='@:1.1.0 +net')
    depends_on('rockets', when='@:1.1.0 +net')
    depends_on('vrpn', when='@:1.1.0 +opendeck')
    depends_on('optix@5.0.1', when='@:1.1.0 +optix')
    depends_on('cuda', when='@:1.1.0 +optix')

    # patch('brion.patch', when='@develop')
    patch('fix_forgotten_algorithm.patch', when='@0.8.0')

    patch('https://patch-diff.githubusercontent.com/raw/BlueBrain/Brayns/pull/938.patch',
          sha256='e1ace3dc7c3dcbea05ea1be90173e0f8ae8401b92b2554114d20b2c6da40eca7',
          when='%gcc@11:')

    patch('https://patch-diff.githubusercontent.com/raw/BlueBrain/Brayns/pull/950.patch',
          sha256='5a43ff4e8ad322aefa5e4ec23fb3bc80ca679d2cd30579caa3d84ad7993bcb10',
          when='@2.0.0%gcc@11:')

    def patch(self):
        cmake_common_file = 'CMake/common/CommonCompiler.cmake'
        if can_access(self.stage.source_path + "/" + cmake_common_file) \
                and self.spec.satisfies('%gcc@9:'):
            filter_file(
                r'-Werror',
                '-Werror -Wno-error=deprecated-copy -Wno-error=range-loop-construct',
                cmake_common_file
            )
        for cmake_filename in find(self.stage.source_path, "CMakeLists.txt"):
            filter_file(r'\$\{GLEW_LIBRARIES\}', 'GLEW', cmake_filename)
        if self.spec.satisfies('@1.0:1.1'):
            filter_file(r'cast<const uint8_t \*const',
                        'cast<const uint8_t *',
                        'plugins/Rockets/encoder.cpp')
        if self.spec.satisfies('@immersive'):
            filter_file(r'(#include <unordered_map>)',
                        '\\1\n#include <functional>',
                        'plugins/VRPN/VRPNPlugin.h')

    def cmake_args(self):
        args = [
            '-DCOMMON_DISABLE_WERROR:BOOL=ON',
            '-DBRAYNS_CIRCUITEXPLORER_ENABLED={0}'.format(
                'ON' if '+brion' in self.spec else 'OFF'),
            '-DBRAYNS_DTI_ENABLED={0}'.format(
                'ON' if '+brion' in self.spec else 'OFF'),
            '-DBRAYNS_CIRCUITINFO_ENABLED={0}'.format(
                'ON' if '+brion' in self.spec else 'OFF'),
            '-DBRAYNS_DEFLECT_ENABLED={0}'.format(
                'ON' if '+deflect' in self.spec else 'OFF')
        ]

        if self.spec.satisfies('@:1.1.0'):
            args.append('-DDISABLE_SUBPROJECTS=ON')
            args.append('-DBRAYNS_NETWORKING_ENABLED={0}'.format(
                'ON' if '+net' in self.spec else 'OFF'))
            args.append('-DBRAYNS_ASSIMP_ENABLED={0}'.format(
                'ON' if '+assimp' in self.spec else 'OFF'))
            args.append('-DBRAYNS_OSPRAY_ENABLED={0}'.format(
                'ON' if '+ospray' in self.spec else 'OFF'))
            args.append('-DBRAYNS_CIRCUITVIEWER_ENABLED={0}'.format(
                'ON' if '+brion' in self.spec else 'OFF'))

            if '+optix' in self.spec:
                args.append('-DBRAYNS_OPTIX_ENABLED=ON')
                args.append('-DBRAYNS_OPTIX_TESTS_ENABLED=ON')

            if '+opendeck' in self.spec:
                args.append('-DBRAYNS_OPENDECK_ENABLED=ON')
                args.append('-DBRAYNS_VRPN_ENABLED=ON')

        return args

    def check(self):
        with working_dir(self.build_directory):
            ninja('tests')

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            if '+optix' in self.spec:
                ninja('braynsOptixEngine')
            ninja()
            if '+doc' in self.spec:
                ninja('doxygen', 'doxycopy')
