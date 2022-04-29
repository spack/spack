# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyMultidict(PythonPackage):
    """Multidict is dict-like collection of key-value pairs where key
    might be occurred more than once in the container."""

    homepage = "https://github.com/aio-libs/multidict"
    pypi     = "multidict/multidict-6.0.2.tar.gz"

    version('6.0.2', sha256='5ff3bd75f38e4c43f1f470f2df7a4d430b821c4ce22be384e1459cb57d6bb013')
    version('5.2.0', sha256='0dd1c93edb444b33ba2274b66f63def8a327d607c6c790772f448a53b6ea59ce')
    version('5.1.0', sha256='25b4e5f22d3a37ddf3effc0710ba692cfc792c2b9edfb9c05aefe823256e84d5')
    version('4.7.6', sha256='fbb77a75e529021e7c4a8d4e823d88ef4d23674a202be4f5addffc72cbb91430')

    depends_on('python@3.7:', when='@6:', type=('build', 'run'))
    depends_on('python@3.6:', when='@5.1:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-pip@18:', when='@:4', type='build')
    depends_on('py-setuptools@40:', type='build')
