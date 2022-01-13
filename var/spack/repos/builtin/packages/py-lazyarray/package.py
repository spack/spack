# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLazyarray(PythonPackage):
    """a Python package that provides a lazily-evaluated numerical array class,
    larray, based on and compatible with NumPy arrays."""

    homepage = "https://lazyarray.readthedocs.io/en/latest/"
    pypi = "lazyarray/lazyarray-0.2.8.tar.gz"

    version('0.3.2',  sha256='be980534c5950a976709085570f69be9534bdf0f3e5c21a9113de3ee2052683e')
    version('0.2.10', sha256='7a53f81b5f3a098c04003d2ad179fc197451fd96bc921510f8534c6af8cc8e19')
    version('0.2.8',  sha256='aaee4e18117cc512de7a4e64522f37bc6f4bf125ecffdbdbf4e4e390fbdd9ba2')

    # Required versions come from doc/installation.txt or:
    # https://lazyarray.readthedocs.io/en/latest/installation.html#dependencies
    depends_on('python@2.7:', when='@0.3:', type=('build', 'run'))
    depends_on('py-numpy@1.3:', type=('build', 'run'))
    depends_on('py-numpy@1.8:', type=('build', 'run'), when='@0.3:')
    depends_on('py-numpy@1.5:', type=('build', 'run'), when='^python@3:')
    depends_on('py-numpy@1.12:', type=('build', 'run'), when='@0.3:^python@3:')
