# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMvdtool(PythonPackage):
    """Python bindings for the MVD3 neuroscience file format parser and tool
    """

    homepage = "https://github.com/BlueBrain/MVDTool"
    git = "https://github.com/BlueBrain/MVDTool.git"
    pypi = "MVDTool/MVDTool-2.4.5.tar.gz"

    submodules = True

    version('develop', branch='master')
    version("2.4.9", sha256="adce0823f102bddf33e2e7dc516f31fbedc12d428c1b205ddf6976c77a2c8962")

    variant('mpi', default=True, description='Build with support for MPI')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('cmake@3.11:', type='build')
    depends_on('py-numpy', type='run')

    depends_on('boost')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5+mpi', type=('build', 'run'), when="+mpi")
    depends_on('hdf5~mpi', type=('build', 'run'), when="~mpi")
    depends_on('libsonata~mpi', type=('build', 'run'), when='~mpi')
    depends_on('libsonata+mpi', type=('build', 'run'), when='+mpi')
    depends_on('highfive~mpi', type='build', when='~mpi')
    depends_on('highfive+mpi', type='build', when='+mpi')
