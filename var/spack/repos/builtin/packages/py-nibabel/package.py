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

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@30.3.0:', type=('build', 'run'))
    depends_on('py-numpy@1.14:', type='run')
    depends_on('py-packaging@14.3:', type='run')
