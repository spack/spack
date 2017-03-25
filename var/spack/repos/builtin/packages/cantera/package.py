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
import os


class Cantera(Package):
    """Cantera is a suite of object-oriented software tools for problems
    involving chemical kinetics, thermodynamics, and/or transport processes."""

    homepage = "http://www.cantera.org/docs/sphinx/html/index.html"
    url      = "https://github.com/Cantera/cantera/archive/v2.2.1.tar.gz"

    version('2.2.1', '9d1919bdef39ddec54485fc8a741a3aa')

    variant('lapack',     default=True,
            description='Build with external BLAS/LAPACK libraries')
    variant('threadsafe', default=True,
            description='Build threadsafe, requires Boost')
    variant('sundials',   default=True,
            description='Build with external Sundials')
    variant('python',     default=False,
            description='Build the Cantera Python module')
    variant('matlab',     default=False,
            description='Build the Cantera Matlab toolbox')

    # Required dependencies
    depends_on('scons', type='build')

    # Recommended dependencies
    depends_on('blas',      when='+lapack')
    depends_on('lapack',    when='+lapack')
    depends_on('boost',     when='+threadsafe')
    depends_on('sundials',  when='+sundials')  # must be compiled with -fPIC

    # Python module dependencies
    extends('python', when='+python')
    depends_on('py-numpy',  when='+python', type=('build', 'run'))
    depends_on('py-scipy',  when='+python', type=('build', 'run'))
    depends_on('py-cython', when='+python', type=('build', 'run'))
    depends_on('py-3to2',   when='+python', type=('build', 'run'))
    # TODO: these "when" specs don't actually work
    # depends_on('py-unittest2',     when='+python^python@2.6', type=('build', 'run'))  # noqa
    # depends_on('py-unittest2py3k', when='+python^python@3.1', type=('build', 'run'))  # noqa

    # Matlab toolbox dependencies
    # TODO: add Matlab package
    # TODO: allow packages to extend multiple other packages
    # extends('matlab',   when='+matlab')

    def install(self, spec, prefix):
        # Required options
        options = [
            'prefix={0}'.format(prefix),
            'CC={0}'.format(os.environ['CC']),
            'CXX={0}'.format(os.environ['CXX']),
            'F77={0}'.format(os.environ['F77']),
            'FORTRAN={0}'.format(os.environ['FC']),
            'cc_flags=-fPIC',
            # Allow Spack environment variables to propagate through to SCons
            'env_vars=all'
        ]

        # BLAS/LAPACK support
        if '+lapack' in spec:
            lapack_blas = spec['lapack'].libs + spec['blas'].libs
            options.extend([
                'blas_lapack_libs={0}'.format(','.join(lapack_blas.names)),
                'blas_lapack_dir={0}'.format(spec['lapack'].prefix.lib)
            ])

        # Threadsafe build, requires Boost
        if '+threadsafe' in spec:
            options.extend([
                'build_thread_safe=yes',
                'boost_inc_dir={0}'.format(spec['boost'].prefix.include),
                'boost_lib_dir={0}'.format(spec['boost'].prefix.lib)
            ])
        else:
            options.append('build_thread_safe=no')

        # Sundials support
        if '+sundials' in spec:
            options.extend([
                'use_sundials=y',
                'sundials_include={0}'.format(spec['sundials'].prefix.include),
                'sundials_libdir={0}'.format(spec['sundials'].prefix.lib),
                'sundials_license={0}'.format(
                    join_path(spec['sundials'].prefix, 'LICENSE'))
            ])
        else:
            options.append('use_sundials=n')

        # Python module
        if '+python' in spec:
            options.extend([
                'python_package=full',
                'python_cmd={0}'.format(
                    join_path(spec['python'].prefix.bin, 'python')),
                'python_array_home={0}'.format(spec['py-numpy'].prefix)
            ])
            if spec['python'].satisfies('@3'):
                options.extend([
                    'python3_package=y',
                    'python3_cmd={0}'.format(
                        join_path(spec['python'].prefix.bin, 'python')),
                    'python3_array_home={0}'.format(spec['py-numpy'].prefix)
                ])
            else:
                options.append('python3_package=n')
        else:
            options.append('python_package=none')
            options.append('python3_package=n')

        # Matlab toolbox
        if '+matlab' in spec:
            options.extend([
                'matlab_toolbox=y',
                'matlab_path={0}'.format(spec['matlab'].prefix)
            ])
        else:
            options.append('matlab_toolbox=n')

        scons('build', *options)

        if '+python' in spec:
            # Tests will always fail if Python dependencies aren't built
            # In addition, 3 of the tests fail when run in parallel
            scons('test', parallel=False)

        scons('install')

        self.filter_compilers()

    def filter_compilers(self):
        """Run after install to tell the Makefile and SConstruct files to use
        the compilers that Spack built the package with.

        If this isn't done, they'll have CC, CXX, F77, and FC set to Spack's
        generic cc, c++, f77, and f90. We want them to be bound to whatever
        compiler they were built with."""

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}
        dirname = os.path.join(self.prefix, 'share/cantera/samples')

        cc_files = [
            'cxx/rankine/Makefile',   'cxx/NASA_coeffs/Makefile',
            'cxx/kinetics1/Makefile', 'cxx/flamespeed/Makefile',
            'cxx/combustor/Makefile', 'f77/SConstruct'
        ]

        cxx_files = [
            'cxx/rankine/Makefile',   'cxx/NASA_coeffs/Makefile',
            'cxx/kinetics1/Makefile', 'cxx/flamespeed/Makefile',
            'cxx/combustor/Makefile'
        ]

        f77_files = [
            'f77/Makefile', 'f77/SConstruct'
        ]

        fc_files = [
            'f90/Makefile', 'f90/SConstruct'
        ]

        for filename in cc_files:
            filter_file(os.environ['CC'], self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cxx_files:
            filter_file(os.environ['CXX'], self.compiler.cxx,
                        os.path.join(dirname, filename), **kwargs)

        for filename in f77_files:
            filter_file(os.environ['F77'], self.compiler.f77,
                        os.path.join(dirname, filename), **kwargs)

        for filename in fc_files:
            filter_file(os.environ['FC'], self.compiler.fc,
                        os.path.join(dirname, filename), **kwargs)
