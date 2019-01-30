# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeo(PythonPackage):
    """Neo is a package for representing electrophysiology data in Python,
    together with support for reading a wide range of neurophysiology
    file formats"""

    homepage = "http://neuralensemble.org/neo"
    url      = "https://pypi.io/packages/source/n/neo/neo-0.4.1.tar.gz"

    version('0.5.2', 'e2b55b112ae245f24cc8ad63cfef986c')
    version('0.4.1', 'f706df3a1bce835cb490b812ac198a6e')

    depends_on('py-setuptools',        type='build')
    depends_on('py-numpy@1.7.1:',      type=('build', 'run'))
    depends_on('py-quantities@0.9.0:', type=('build', 'run'))
