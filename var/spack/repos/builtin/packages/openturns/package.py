# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openturns(CMakePackage):
    """OpenTURNS is a scientific C++ and Python library featuring an
    internal data model and algorithms dedicated to the treatment of
    uncertainties. The main goal of this library is to provide all
    functionalities needed to treat uncertainties in studies with
    industrial applications. Targeted users are all engineers who want
    to introduce the probabilistic dimension in their so far
    deterministic studies."""

    homepage = "https://openturns.github.io/www/"
    url      = "https://github.com/openturns/openturns/archive/refs/tags/v1.18.tar.gz"
    git      = "https://github.com/openturns/openturns.git"
    maintainers = ['liuyangzhuan']

    version('1.18', sha256='1840d3fd8b38fd5967b1fa04e49d8f760c2c497400430e97623595ca48754ae0')
    version('master', branch='master')

    variant('python',   default=True,  description='Build Python bindings')

    extends('python', when='+python')

    depends_on('mpi', type=('build', 'run'))
    depends_on('lapack', type=('build', 'run'))
    depends_on('cmake@2.8:', type='build')
    depends_on('swig', type=('build', 'run'))
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('boost+system+serialization+thread', type=('build', 'run'))
    depends_on('intel-tbb', type=('build', 'run'))
    depends_on('py-cloudpickle', type=('build', 'run'))
    depends_on('py-urllib3', type=('build', 'run'))

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_INSTALL_LIBDIR:STRING=%s' % self.prefix.lib,
            '-DCMAKE_INSTALL_BINDIR:STRING=%s' % self.prefix.bin,
            '-DLAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(";"),
        ]

        if '+python' in spec:
            args.extend([
                # By default picks up the system python not the Spack build
                '-DPYTHON_EXECUTABLE={0}'.format(spec['python'].command.path),
                # By default installs to the python prefix
                '-DPYTHON_SITE_PACKAGES={0}'.format(python_platlib),
            ])

        return args
