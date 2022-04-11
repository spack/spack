# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLibsonata(PythonPackage):
    """SONATA files reader"""

    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"

    version('develop', branch='master', submodules=True, get_full_repo=True)
    version('0.1.12', tag='v0.1.12', submodules=True, get_full_repo=True)
    version('0.1.11', tag='v0.1.11', submodules=True, get_full_repo=True)
    version('0.1.10', tag='v0.1.10', submodules=True, get_full_repo=True)
    # Important: v0.1.9 is not Spack-compatible (use v0.1.10: instead)
    # version('0.1.9', tag='v0.1.9', submodules=True, get_full_repo=True)
    version('0.1.8', tag='v0.1.8', submodules=True, get_full_repo=True)
    version('0.1.6', tag='v0.1.6', submodules=True, get_full_repo=True)
    version('0.1.5', tag='v0.1.5', submodules=True, get_full_repo=True)
    version('0.1.4', tag='v0.1.4', submodules=True, get_full_repo=True)
    version('0.1.3', tag='v0.1.3', submodules=True, get_full_repo=True)
    version('0.1.0', tag='v0.1.0', submodules=True, get_full_repo=True)
    version('0.0.3', tag='v0.0.3', submodules=True)

    depends_on('cmake@3.3:', type='build')
    depends_on('hdf5')
    depends_on('py-pybind11')

    depends_on('py-numpy@1.12:', type=('build', 'run'))
    depends_on('py-setuptools', type='build', when='@0.1:')
    depends_on('py-setuptools-scm', type='build', when='@0.1:')
