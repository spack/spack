# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPybigwig(PythonPackage):
    """A package for accessing bigWig files using libBigWig."""

    homepage = "https://pypi.python.org/pypi/pyBigWig"
    url      = "https://pypi.io/packages/source/p/pyBigWig/pyBigWig-0.3.4.tar.gz"

    version('0.3.4', '8e0a91e26e87eeaa071408a3a749bfa9')

    depends_on('py-setuptools', type='build')
    depends_on('curl', type=('build', 'run'))
