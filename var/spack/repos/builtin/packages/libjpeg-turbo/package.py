# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibjpegTurbo(Package):
    """libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to
       accelerate baseline JPEG compression and decompression. libjpeg is a
       library that implements JPEG image encoding, decoding and
       transcoding."""
    # https://github.com/libjpeg-turbo/libjpeg-turbo/blob/master/BUILDING.md
    homepage = "https://libjpeg-turbo.org/"
    url      = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/2.0.2.tar.gz"

    version('2.0.2', sha256='b45255bd476c19c7c6b198c07c0487e8b8536373b82f2b38346b32b4fa7bb942')
    version('1.5.90', '85f7f9c377b70cbf48e61726097d4efa')
    version('1.5.3', '5b7549d440b86c98a517355c102d155e')
    version('1.5.0', 'eff98ac84de05eafc65ae96caa6e23e9')
    version('1.3.1', '5e4bc19c3cb602bcab1296b9bee5124c')

    provides('jpeg')

    # Can use either of these. But in the current version of the package
    # only nasm is used. In order to use yasm an environmental variable
    # NASM must be set.
    # TODO: Implement the selection between two supported assemblers.
    # depends_on("yasm", type='build')
    depends_on("nasm", type='build')
    depends_on('autoconf', type='build', when="@1.3.1:1.5.3")
    depends_on('automake', type='build', when="@1.3.1:1.5.3")
    depends_on('libtool', type='build', when="@1.3.1:1.5.3")
    depends_on('cmake', type='build', when="@1.5.90:")

    @property
    def libs(self):
        return find_libraries("libjpeg*", root=self.prefix, recursive=True)

    def flag_handler(self, name, flags):
        if self.spec.satisfies('@1.5.90:'):
            return (None, None, flags)
        else:
            # compiler flags for earlier version are injected into the
            # spack compiler wrapper
            return (flags, None, None)

    def flags_to_build_system_args(self, flags):
        # This only handles cflags, other flags are discarded
        cmake_flag_args = []
        if 'cflags' in flags and flags['cflags']:
            cmake_flag_args.append('-DCMAKE_C_FLAGS={0}'.format(
                                   ' '.join(flags['cflags'])))
        self.cmake_flag_args = cmake_flag_args

    @when('@1.3.1:1.5.3')
    def install(self, spec, prefix):
        autoreconf('-ifv')
        configure('--prefix=%s' % prefix)
        make()
        make('install')

    @when('@1.5.90:')
    def install(self, spec, prefix):
        cmake_args = ['-GUnix Makefiles']
        if hasattr(self, 'cmake_flag_args'):
            cmake_args.extend(self.cmake_flag_args)
        cmake_args.extend(std_cmake_args)
        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')
