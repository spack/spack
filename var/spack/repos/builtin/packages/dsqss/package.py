# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import glob


class Dsqss(CMakePackage):
    """DSQSS is a program package for solving quantum many-body
    problems defined on lattices. It is based on the quantum Monte
    Carlo method in Feynman’s path integral representation. """

    homepage = "https://www.pasums.issp.u-tokyo.ac.jp/dsqss/en/"
    url      = "https://github.com/issp-center-dev/dsqss/releases/download/v2.0.3/dsqss-v2.0.3.tar.gz"

    version('2.0.3', sha256='11255dd1f1317fb4ac2d6ae95535f027d627d03f5470717cd277dd9ab94496e0')

    depends_on('mpi')
    depends_on('python', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-toml', type=('build', 'run'))

    patch('ctest.patch')

    @run_before('cmake')
    def rm_macos(self):
        macpath = 'test/*/._*.json'
        r = glob.glob(macpath)
        for i in r:
            os.remove(i)

    def cmake_args(self):
        args = []
        args.append('-DCMAKE_INSTALL_PREFIX=%s' % self.spec.prefix)
        return args

    def setup_run_environment(self, env):
        python_version = self.spec['python'].version.up_to(2)
        env.prepend_path('PYTHONPATH', join_path(
                         self.prefix,
                         'lib',
                         'python{0}'.format(python_version),
                         'site-packages'))
