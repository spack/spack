# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyLibensemble(PythonPackage):
    """Library for managing ensemble-like collections of computations."""

    homepage = "https://libensemble.readthedocs.io"
    url      = "https://pypi.io/packages/source/l/libensemble/libensemble-0.3.0.tar.gz"
    git      = "https://github.com/Libensemble/libensemble.git"

    version('develop', branch='master')
    version('0.3.0', sha256='c8efdf45d0da0ef6299ee778cea1c285c95972af70d3a729ee6dc855e66f9294')
    version('0.2.0', 'ee96047594a3f5a1533f24d3b1f365f9')
    version('0.1.0', '0c3d45dd139429de1a5273e5bd8e46ec')

    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-setuptools', type='build')
    depends_on('mpi')
    depends_on('py-mpi4py@2.0:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-petsc4py@3.5:', type=('build', 'run'))
    depends_on('nlopt', type=('build', 'run'))
