# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLibsonata(PythonPackage):
    """SONATA files reader"""

    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"

    version('0.0.3', commit='fd77f22d94737593f8ac86aa762d25a8b8622100', submodules=True)
    version('0.0.2', commit='3ebd44e802b5b46008b255ec0c1e2f0eabdf6ac6', submodules=True)

    depends_on('cmake@3.3:', type='build')
    depends_on('hdf5~mpi', type='build')

    depends_on('py-numpy@1.12:', type='run')
