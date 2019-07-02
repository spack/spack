# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMvdtool(PythonPackage):
    """Python bindings for the MVD3 neuroscience file format parser and tool
    """

    homepage = "https://github.com/BlueBrain/MVDTool"
    url      = "https://github.com/BlueBrain/MVDTool.git"
    git      = "https://github.com/BlueBrain/MVDTool.git"

    version('develop', branch='master', submodules=True, clean=False)
    version('2.0.0', tag='v2.0.0', submodules=True, clean=False)

    depends_on('py-setuptools', type='build')

    depends_on('cmake@3.2:', type='build')
    depends_on('py-numpy', type='run')
    depends_on('hdf5~mpi', type=('build', 'run'))
    depends_on('highfive', type='build')
