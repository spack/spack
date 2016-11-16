##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Symengine(Package):
    """SymEngine is a fast symbolic manipulation library, written in C++."""

    homepage = "https://github.com/symengine/symengine"
    url      = "https://github.com/symengine/symengine/archive/v0.2.0.tar.gz"

    version('0.2.0', '45401561add36a13c1f0b0c5f8d7422d')
    version('0.1.0', '41ad7daed61fc5a77c285eb6c7303425')
    version('develop', git='https://github.com/symengine/symengine.git')

    variant('flint',        default=True,
            description='Compile with Flint integer library')
    variant('mpc',          default=True,
            description='Compile with MPC library')
    variant('mpfr',         default=True,
            description='Compile with MPFR library')
    variant('piranha',      default=False,
            description='Compile with Piranha integer library')
    variant('thread_safe',  default=True,
            description='Enable thread safety option')
    variant('openmp',       default=False,
            description='Enable OpenMP support')
    variant('shared',       default=True,
            description='Enables the build of shared libraries')

    # Build dependencies
    depends_on('cmake',    type='build')

    # Other dependencies
    depends_on('gmp')  # mpir is a drop-in replacement for this
    depends_on('mpc',      when='+mpc')  # Could also be built against mpir
    depends_on('mpfr',     when='+mpfr')  # Could also be built against mpir
    depends_on('flint',    when='+flint')  # Could also be built against mpir
    depends_on('piranha',  when='+piranha~flint')  # Could also be built against mpir  # NOQA

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        # CMAKE_BUILD_TYPE should be Debug | Release
        for word in options[:]:
            if word.startswith('-DCMAKE_BUILD_TYPE'):
                options.remove(word)

        # See https://github.com/symengine/symengine/blob/master/README.md
        # for build options
        options.extend([
            '-DCMAKE_BUILD_TYPE=Release',
            '-DWITH_SYMENGINE_RCP:BOOL=ON',
            '-DWITH_SYMENGINE_THREAD_SAFE:BOOL=%s' % (
                'ON' if ('+thread_safe' or '+openmp') in spec else 'OFF'),
            '-DBUILD_TESTS:BOOL=ON',
            '-DBUILD_BENCHMARKS:BOOL=ON',
            '-DWITH_MPC:BOOL=%s' % (
                'ON' if '+mpc' in spec else 'OFF'),
            '-DWITH_MPFR:BOOL=%s' % (
                'ON' if '+mpfr' in spec else 'OFF'),
            '-DINTEGER_CLASS:STRING=gmp',
            '-DWITH_OPENMP:BOOL=%s' % (
                'ON' if '+openmp' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
        ])

        if '+flint' in spec:
            options.extend([
                '-DWITH_FLINT:BOOL=ON',
                '-DINTEGER_CLASS:STRING=flint'
            ])
        elif '+piranha' in spec:
            options.extend([
                '-DWITH_PIRANHA:BOOL=ON',
                '-DINTEGER_CLASS:STRING=piranha'
            ])
        else:
            options.extend([
                '-DINTEGER_CLASS:STRING=gmp'
            ])

        with working_dir('spack-build', create=True):
            cmake('..', *options)

            make()
            make('install')
            if self.run_tests:
                ctest()
