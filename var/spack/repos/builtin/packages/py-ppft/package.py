# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPpft(PythonPackage):
    """Distributed and parallel python """

    homepage = "https://github.com/uqfoundation/ppft"
    url      = "https://pypi.io/packages/source/p/ppft/ppft-1.6.4.7.1.zip"

    version('1.6.4.7.1',  sha256='f94b26491b4a36adc975fc51dba7568089a24756007a3a4ef3414a98d7337651')
    version('1.6.4.6',   sha256='92d09061f5425634c43dbf99c5558f2cf2a2e1e351929f8da7e85f4649c11095')
    version('1.6.4.5',   sha256='d47da9d2e553848b75727ce7c510f9e149965d5c68f9fc56c774a7c6a3d18214')

    depends_on('python@2.5:2.8,3.1:')

    depends_on('py-setuptools@0.6:', type='build')
    depends_on('py-six@1.7.3:', type=('build', 'run'))
    depends_on('py-dill@0.2.6:', type=('build', 'run'))
