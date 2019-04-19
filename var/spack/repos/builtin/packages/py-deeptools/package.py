# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeeptools(PythonPackage):
    """deepTools addresses the challenge of handling the large amounts of data
       that are now routinely generated from DNA sequencing centers."""

    homepage = "https://pypi.io/packages/source/d/deepTools"
    url      = "https://pypi.io/packages/source/d/deepTools/deepTools-2.5.2.tar.gz"

    version('3.2.1', sha256='ccbabb46d6c17c927e96fadc43d8d4770efeaf40b9bcba3b94915a211007378e')
    version('2.5.2', 'ba8a44c128c6bb1ed4ebdb20bf9ae9c2')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.9.0:', type=('build', 'run'))
    depends_on('py-scipy@0.17.0:', type=('build', 'run'))
    depends_on('py-py2bit@0.2.0:', type=('build', 'run'))
    depends_on('py-pybigwig@0.2.1:', type=('build', 'run'))
    depends_on('py-pysam@0.8.2:', type=('build', 'run'))
    depends_on('py-matplotlib@1.4.0:', type=('build', 'run'))
    depends_on('py-numpydoc@0.5:', type=('build', 'run'))
