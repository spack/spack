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


class Psi4(Package):
    """Psi4 is an open-source suite of ab initio quantum chemistry
    programs designed for efficient, high-accuracy simulations of
    a variety of molecular properties."""

    homepage = "http://www.psicode.org/"
    url = "https://github.com/psi4/psi4/archive/0.5.tar.gz"

    version('0.5', '53041b8a9be3958384171d0d22f9fdd0')

    # Required dependencies
    depends_on('blas')
    depends_on('lapack')
    depends_on('boost'
               '+chrono'
               '+filesystem'
               '+python'
               '+regex'
               '+serialization'
               '+system'
               '+timer'
               '+thread')
    depends_on('python')
    depends_on('cmake', type='build')
    depends_on('py-numpy', type=('build', 'run'))

    # Optional dependencies
    # TODO: add packages for these
    # depends_on('perl')
    # depends_on('erd')
    # depends_on('pcm-solver')
    # depends_on('chemps2')

    def install(self, spec, prefix):
        cmake_args = [
            '-DBLAS_TYPE={0}'.format(spec['blas'].name.upper()),
            '-DBLAS_LIBRARIES={0}'.format(spec['blas'].libs.joined()),
            '-DLAPACK_TYPE={0}'.format(spec['lapack'].name.upper()),
            '-DLAPACK_LIBRARIES={0}'.format(
                spec['lapack'].libs.joined()),
            '-DBOOST_INCLUDEDIR={0}'.format(spec['boost'].prefix.include),
            '-DBOOST_LIBRARYDIR={0}'.format(spec['boost'].prefix.lib),
            '-DENABLE_CHEMPS2=OFF'
        ]

        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)

            make()
            make('install')

        self.filter_compilers(spec, prefix)

    def filter_compilers(self, spec, prefix):
        """Run after install to tell the configuration files to
        use the compilers that Spack built the package with.

        If this isn't done, they'll have PLUGIN_CXX set to
        Spack's generic cxx. We want it to be bound to
        whatever compiler it was built with."""

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}

        cc_files = ['bin/psi4-config']
        cxx_files = ['bin/psi4-config', 'include/psi4/psiconfig.h']
        template = 'share/psi4/plugin/Makefile.template'

        for filename in cc_files:
            filter_file(os.environ['CC'], self.compiler.cc,
                        os.path.join(prefix, filename), **kwargs)

        for filename in cxx_files:
            filter_file(os.environ['CXX'], self.compiler.cxx,
                        os.path.join(prefix, filename), **kwargs)

        # The binary still keeps track of the compiler used to install Psi4
        # and uses it when creating a plugin template
        filter_file('@PLUGIN_CXX@', self.compiler.cxx,
                    os.path.join(prefix, template), **kwargs)

        # The binary links to the build include directory instead of the
        # installation include directory:
        # https://github.com/psi4/psi4/issues/410
        filter_file('@PLUGIN_INCLUDES@', '-I{0}'.format(
            ' -I'.join([
                os.path.join(spec['psi4'].prefix.include, 'psi4'),
                os.path.join(spec['boost'].prefix.include, 'boost'),
                os.path.join(spec['python'].prefix.include, 'python{0}'.format(
                    spec['python'].version.up_to(2))),
                spec['lapack'].prefix.include,
                spec['blas'].prefix.include,
                '/usr/include'
            ])
        ), os.path.join(prefix, template), **kwargs)
