# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyMrcfile(PythonPackage):
    """Python implementation of the MRC2014 file format, which is used
    in structural biology to store image and volume data."""

    homepage = "https://github.com/ccpem/mrcfile/"
    url      = "https://github.com/ccpem/mrcfile/archive/refs/tags/v1.3.0.tar.gz"

    maintainers = ['dorton21']

    version('1.3.0', sha256='034f1868abf87f4e494b8b039030b50045cabccf352b8b3e88a6bd3a6d665715')

    depends_on('python@3.4.0:')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.12.0:', type=('build', 'run'))
