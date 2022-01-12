# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyvista(PythonPackage):
    """Easier Pythonic interface to VTK."""

    homepage = "https://github.com/pyvista/pyvista"
    pypi     = "pyvista/pyvista-0.32.1.tar.gz"

    version('0.32.1', sha256='585ac79524e351924730aff9b7207d6c5ac4175dbb5d33f7a9a2de22ae53dbf9')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-imageio', type=('build', 'run'))
    depends_on('pil', type=('build', 'run'))
    depends_on('py-appdirs', type=('build', 'run'))
    depends_on('py-scooby@0.5.1:', type=('build', 'run'))
    depends_on('py-meshio@4.0.3:4', type=('build', 'run'))
    depends_on('vtk+python', type=('build', 'run'))
    depends_on('py-dataclasses', when='^python@3.6', type=('build', 'run'))
    depends_on('py-typing-extensions', type=('build', 'run'))
