# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTqdm(PythonPackage):
    """A Fast, Extensible Progress Meter"""

    homepage = "https://github.com/tqdm/tqdm"
    url      = "https://pypi.io/packages/source/t/tqdm/tqdm-4.8.4.tar.gz"

    version('4.8.4', sha256='bab05f8bb6efd2702ab6c532e5e6a758a66c0d2f443e09784b73e4066e6b3a37')

    depends_on('py-setuptools', type='build')
