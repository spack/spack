# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySlepc4py(PythonPackage):
    """This package provides Python bindings for the SLEPc package.
    """
    homepage = "https://pypi.python.org/pypi/slepc4py"
    url      = "https://pypi.io/packages/source/s/slepc4py/slepc4py-3.7.0.tar.gz"

    version('3.7.0', 'c4775e88b0825c7313629c01de60ecb2')

    depends_on('py-setuptools', type='build')
    depends_on('py-petsc4py', type=('build', 'run'))
    depends_on('slepc')
