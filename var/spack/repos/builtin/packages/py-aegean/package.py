# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAegean(PythonPackage):
    """py-aegean (Aegean software tools) is a Aegean source finding package
    for radio astronomy researchers."""

    homepage = "https://github.com/PaulHancock/Aegean"
    url      = "https://github.com/PaulHancock/Aegean/archive/v2.1.1.tar.gz"

    version('2.1.1', sha256='ada54ee85911410f6db3e66758753f5b4c9c7a4420c3a1d677e04cdeb7339a28')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-lmfit', type=('build', 'run'))
    depends_on('py-astropy', type=('build', 'run'))
