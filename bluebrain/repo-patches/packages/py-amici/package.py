# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAmici(PythonPackage):
    """Advanced Multilanguage Interface for CVODES and IDAS"""

    homepage = "https://github.com/AMICI-dev/AMICI"
    pypi     = "amici/amici-0.11.28.tar.gz"

    version('0.11.28', sha256='a8ddda70d8ebdc40600b4ad2ea02eb26e765ca0e594b957f61866b8c84255d5b')

    depends_on('cmake', type=('build', 'run'))
    depends_on('blas', type=('build', 'run'))
    depends_on('boost')
    depends_on('hdf5+cxx+hl', type=('build', 'run'))
    depends_on('swig', type=('build', 'run'))

    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-pkgconfig', type=('build', 'run'))
    depends_on('py-python-libsbml', type=('build', 'run'))
    depends_on('py-sympy@1.9:', type=('build', 'run'))
    depends_on('py-toposort', type=('build', 'run'))
    depends_on('py-wurlitzer', type=('build', 'run'))

    def setup_run_environment(self, env):
        env.set("BLAS_LIBS", " ".join(self.spec['blas'].libs))

    def setup_build_environment(self, env):
        env.set("BLAS_LIBS", " ".join(self.spec['blas'].libs))
