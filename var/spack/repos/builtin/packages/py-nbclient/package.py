# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *


class PyNbclient(PythonPackage):
    """A client library for executing notebooks.

    Formally nbconvert's ExecutePreprocessor."""

    homepage = "https://jupyter.org/"
    pypi = "nbclient/nbclient-0.5.0.tar.gz"

    version('0.5.5', sha256='ed7d18431393750d29a64da432e0b7889274eb5a5056682be5691b1b1dc8f755')
    version('0.5.0', sha256='8ad52d27ba144fca1402db014857e53c5a864a2f407be66ca9d74c3a56d6591d')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('python@3.6.1:', type=('build', 'run'), when='@0.5.5:')
    depends_on('py-setuptools', type='build')
    depends_on('py-traitlets@4.2:', type=('build', 'run'))
    depends_on('py-jupyter-client@6.1.5:', type=('build', 'run'))
    depends_on('py-nbformat@5.0:', type=('build', 'run'))
    depends_on('py-async-generator', type=('build', 'run'), when='@0.5.0')
    depends_on('py-async-generator', type=('build', 'run'), when='@0.5.5: ^python@:3.6')
    depends_on('py-nest-asyncio', type=('build', 'run'))
