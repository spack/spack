# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLibsonata(PythonPackage):
    """SONATA files reader"""

    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"

    version('0.1.5', tag='v0.1.5', submodules=True, get_full_repo=True)
    version('0.1.4', tag='v0.1.4', submodules=True, get_full_repo=True)
    version('0.1.3', tag='v0.1.3', submodules=True, get_full_repo=True)
    version('0.1.0', tag='v0.1.0', submodules=True, get_full_repo=True)
    version('0.0.3', tag='v0.0.3', submodules=True)

    depends_on('cmake@3.3:', type='build')
    depends_on('hdf5~mpi')
    depends_on('py-pybind11')

    depends_on('py-numpy@1.12:', type=('build', 'run'))
    depends_on('py-setuptools', type='build', when='@0.1:')
