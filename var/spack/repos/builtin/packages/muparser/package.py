# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Muparser(Package):
    """C++ math expression parser library."""
    homepage = "http://muparser.beltoforion.de/"
    url      = "https://github.com/beltoforion/muparser/archive/v2.2.5.tar.gz"

    version('2.2.6.1', '410d29b4c58d1cdc2fc9ed1c1c7f67fe')
    # 2.2.6 presents itself as 2.2.5, don't add it to Spack
    # version('2.2.6', 'f197b2815ca0422b2091788a78f2dc8a')
    version('2.2.5', '02dae671aa5ad955fdcbcd3fee313fb7')

    # Replace std::auto_ptr by std::unique_ptr
    # https://github.com/beltoforion/muparser/pull/46
    patch('auto_ptr.patch',
          when='@2.2.5')

    depends_on('cmake@3.1.0:', when='@2.2.6:', type='build')

    # Cmake build since 2.2.6
    @when('@2.2.6:')
    def install(self, spec, prefix):
        cmake_args = [
            '-DENABLE_SAMPLES=OFF',
            '-DENABLE_OPENMP=OFF',
            '-DBUILD_SHARED_LIBS=ON'
        ]

        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')

    @when('@2.2.5')
    def install(self, spec, prefix):
        options = ['--disable-debug',
                   '--disable-samples',
                   '--disable-dependency-tracking',
                   'CXXFLAGS={0}'.format(self.compiler.cxx11_flag),
                   '--prefix=%s' % prefix]

        configure(*options)

        make(parallel=False)
        make("install")
