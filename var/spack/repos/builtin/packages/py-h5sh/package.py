# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyH5sh(PythonPackage):
    """Shell-like environment for HDF5."""

    homepage = "https://h5sh.readthedocs.io/en/"
    url      = "https://github.com/sethrj/h5sh/archive/v0.1.0.tar.gz"

    maintainers = ['sethrj']

    version('0.1.0', sha256='52d672e3140323e51084a1bfa2d84012e23c640469242381090a3c7af3e00e4f')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-h5py@2.7.1:', type=('build', 'run'))
    depends_on('py-numpy@1.15:', type=('build', 'run'))
    depends_on('py-prompt-toolkit@2:', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
