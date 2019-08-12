# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJpype(PythonPackage):
    """JPype is an effort to allow python programs full access to java class
    libraries."""

    homepage = "https://github.com/originell/jpype"
    url      = "https://pypi.io/packages/source/J/JPype1/JPype1-0.6.2.tar.gz"

    version('0.6.2', '16e5ee92b29563dcc63bbc75556810c1')
    version('0.6.1', '468ca2d4b2cff7802138789e951d5d58')
    version('0.6.0', 'f0cbbe1d0c4b563f7e435d2bffc31736')

    depends_on('python@2.6:')

    depends_on('py-setuptools', type='build')
    depends_on('java', type=('build', 'run'))
    # extra requirements
    # depends_on('py-numpy@1.6:', type=('build', 'run'))
