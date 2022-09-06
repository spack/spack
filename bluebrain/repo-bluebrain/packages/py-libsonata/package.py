# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibsonata(PythonPackage):
    """SONATA files reader"""

    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"

    version('develop', branch='master', submodules=True, get_full_repo=True)
    version('0.1.14', tag='v0.1.14', submodules=True, get_full_repo=True)
    version('0.1.13', tag='v0.1.13', submodules=True, get_full_repo=True)
    version('0.1.12', tag='v0.1.12', submodules=True, get_full_repo=True)
    version('0.1.11', tag='v0.1.11', submodules=True, get_full_repo=True)
    version('0.1.10', tag='v0.1.10', submodules=True, get_full_repo=True)

    depends_on('cmake@3.3:', type='build')
    depends_on('hdf5')
    depends_on('py-pybind11')

    depends_on('py-numpy@1.17:', type=('build', 'run'))
    depends_on('py-setuptools', type='build', when='@0.1:')
    depends_on('py-setuptools-scm', type='build', when='@0.1:')
