# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyScikitBuild(PythonPackage):
    """scikit-build is an improved build system generator for CPython
       C/C++/Fortran/Cython extensions. It provides better support for
       additional compilers, build systems, cross compilation, and
       locating dependencies and their associated build requirements.

       The scikit-build package is fundamentally just glue between
       the setuptools Python module and CMake."""

    homepage = "https://scikit-build.readthedocs.io/en/latest/"
    url      = "https://github.com/scikit-build/scikit-build/archive/0.10.0.tar.gz"

    maintainers = ['coreyjadams']

    version('0.12.0', sha256='c32a415d2e7920a4a966b037403c93b02c8a958d8badf3c60abd4b4493f7d988')
    version('0.10.0', sha256='2beec252813b20327072c15e9d997f15972aedcc6a130d0154979ff0fdb1b010')

    depends_on('py-setuptools@28.0.0:', type=('build', 'run'))
    depends_on('py-packaging',  type=('build', 'run'))
    depends_on('py-wheel@0.29.0:', type=('build', 'run'))
    depends_on('py-distro', type=('build', 'run'), when='@0.11:')
