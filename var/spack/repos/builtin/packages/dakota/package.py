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


class Dakota(Package):
    """
    The Dakota toolkit provides a flexible, extensible interface between analysis codes and iterative systems
    analysis methods. Dakota contains algorithms for:

    - optimization with gradient and non gradient-based methods;
    - uncertainty quantification with sampling, reliability, stochastic expansion, and epistemic methods;
    - parameter estimation with nonlinear least squares methods;
    - sensitivity/variance analysis with design of experiments and parameter study methods.

    These capabilities may be used on their own or as components within advanced strategies such as hybrid optimization,
    surrogate-based optimization, mixed integer nonlinear programming, or optimization under uncertainty.
    """

    homepage = 'https://dakota.sandia.gov/'
    url = 'https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.3-public.src.tar.gz'
    _url_str = 'https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-{version}-public.src.tar.gz'

    version('6.3', '05a58d209fae604af234c894c3f73f6d')

    variant('debug', default=False, description='Builds a debug version of the libraries')
    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('mpi', default=True, description='Activates MPI support')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')

    depends_on('python')
    depends_on('boost')

    def url_for_version(self, version):
        return Dakota._url_str.format(version=version)

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        options.extend(['-DCMAKE_BUILD_TYPE:STRING=%s' % ('Debug' if '+debug' in spec else 'Release'),
                        '-DBUILD_SHARED_LIBS:BOOL=%s' % ('ON' if '+shared' in spec else 'OFF')])

        if '+mpi' in spec:
            options.extend(['-DDAKOTA_HAVE_MPI:BOOL=ON',
                            '-DMPI_CXX_COMPILER:STRING=%s' % join_path(spec['mpi'].prefix.bin, 'mpicxx')])

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make("install")
