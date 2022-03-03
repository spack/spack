# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycompadre(PythonPackage):
    """The Compadre Toolkit provides a performance portable solution for the
    parallel evaluation of computationally dense kernels. The toolkit
    specifically targets the Generalized Moving Least Squares (GMLS) approach,
    which requires the inversion of small dense matrices. The result is a set
    of weights that provide the information needed for remap or entries that
    constitute the rows of some globally sparse matrix.
    """

    homepage    = 'https://github.com/SNLComputation/compadre'
    git         = 'https://github.com/SNLComputation/compadre.git'
    url         = 'https://github.com/SNLComputation/compadre/archive/v1.3.0.tar.gz'
    maintainers = ['kuberry']

    version('master',  branch='master', preferred=True)

    variant('trilinos', default=False, description='Use Kokkos from Trilinos')

    depends_on('cmake@3.10.0:', type='build')
    depends_on('python@3.4:', type=('build', 'link', 'run'))
    depends_on('py-pip', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.23:', type='build')
    depends_on('trilinos@13.2:', when='+trilinos')

    @run_before('install')
    def set_kokkos(self):
        spec = self.spec
        with open('cmake_opts.txt', 'w') as f:
            if '+trilinos' in spec:
                f.write('Trilinos_PREFIX:PATH=%s\n' % spec['trilinos'].prefix)
