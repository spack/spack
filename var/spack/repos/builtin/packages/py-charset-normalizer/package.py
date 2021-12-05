# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCharsetNormalizer(PythonPackage):
    """The Real First Universal Charset Detector. Open, modern and actively
    maintained alternative to Chardet."""

    homepage = 'https://github.com/ousret/charset_normalizer'
    pypi     = 'charset-normalizer/charset-normalizer-2.0.7.tar.gz'

    version('2.0.7', sha256='e019de665e2bcf9c2b64e2e5aa025fa991da8720daa3c1138cadd2fd1856aed0')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
