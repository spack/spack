# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNibabel(PythonPackage):
    """Access a multitude of neuroimaging data formats"""

    homepage = "https://nipy.org/nibabel"
    pypi     = "nibabel/nibabel-3.2.1.tar.gz"

    version('3.2.1', sha256='4d2ff9426b740011a1c916b54fc25da9348282e727eaa2ea163f42e00f1fc29e')
    version('2.4.1', sha256='f165ff1cb4464902d6594eb2694e2cfb6f8b9fe233b856c976c3cff623ee0e17')

    depends_on('python@3.6:', when='@3.1', type=('build', 'run'))
    depends_on('py-setuptools@30.3.0:', type=('build', 'run'))
    depends_on('py-numpy@1.14:', when='@3.2:', type='run')
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-packaging@14.3:', when='@3.1:', type='run')
    depends_on('py-six@1.3:', when='@:2.5', type='run')
    depends_on('py-bz2file', when='@:2.5 ^python@:2', type='run')
