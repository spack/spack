# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import sys


class Dsqss(CMakePackage):
    """DSQSS is a program package for solving quantum many-body
    problems defined on lattices. It is based on the quantum Monte
    Carlo method in Feynman's path integral representation. """

    homepage = "https://www.pasums.issp.u-tokyo.ac.jp/dsqss/en/"
    url      = "https://github.com/issp-center-dev/dsqss/releases/download/v2.0.3/dsqss-v2.0.3.tar.gz"

    version('2.0.3', sha256='11255dd1f1317fb4ac2d6ae95535f027d627d03f5470717cd277dd9ab94496e0')

    variant("mpi", default=True, description="build mpi support")

    depends_on('mpi', when='+mpi')
    depends_on('python', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-toml', type=('build', 'run'))

    patch('ctest.patch')

    extends('python')

    @run_before('cmake')
    def rm_macos(self):
        if sys.platform != 'darwin':
            for mfile in find('test', '._*.json', recursive=True):
                force_remove(mfile)

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.append('-DENABLE_MPI=ON')
        else:
            args.append('-DENABLE_MPI=OFF')

        return args
