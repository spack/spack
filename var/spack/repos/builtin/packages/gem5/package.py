# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gem5(SConsPackage):
    """The gem5 simulator is a modular platform for computer-system
    architecture research, encompassing system-level architecture as
    well as processor microarchitecture."""

    homepage = "https://www.gem5.org/"
    git      = "https://gem5.googlesource.com/public/gem5"

    version('master', branch='master')

    variant('variant', default='opt',
            description='Compilation settings',
            values=('debug', 'opt', 'fast', 'prof', 'perf'))
    variant('protobuf', default=True, description='Enable trace generation and playback')
    variant('boost', default=True, description='Use the SystemC implementation')

    # https://www.gem5.org/documentation/general_docs/building
    # http://www.m5sim.org/Dependencies
    depends_on('python@2.7:2.8', type=('build', 'link', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('scons@0.98.1:', type='build')
    depends_on('zlib')
    depends_on('pkgconfig', type='build')

    depends_on('protobuf@2.1:', when='+protobuf')
    depends_on('boost', when='+boost')

    conflicts('%gcc@:4.7')
    conflicts('%clang@:3.0')

    def setup_build_environment(self, env):
        # SCons clears environment variables, so we can't use compiler wrappers
        env.set('CC',  self.compiler.cc)
        env.set('CXX', self.compiler.cxx)

        # Specify dependency prefixes
        env.set('PYTHON_CONFIG', self.spec['python'].command.path + '-config')
        env.prepend_flag('LDFLAGS_EXTRA', self.spec['python'].libs.ld_flags)

        if '+profobuf' in self.spec:
            env.set('PROTOC', self.spec['protobuf'].prefix.bin.protoc)

    def build_args(self, spec, prefix):
        # TODO: support more ISAs (ARCH, ARM, NULL, MIPS, POWER, SPARC, X86)
        args = [
            'build/X86/gem5.' + spec.variants['variant'].value,
            '-j', str(make_jobs),
            '--ignore-style',
            '--verbose',
        ]
        return args
