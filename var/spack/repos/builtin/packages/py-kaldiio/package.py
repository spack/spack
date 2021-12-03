# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKaldiio(PythonPackage):
    """A pure python module for reading and writing kaldi ark files"""

    homepage = "https://github.com/nttcslab-sp/kaldiio"
    url      = "https://github.com/nttcslab-sp/kaldiio/archive/refs/tags/v2.17.2.zip"

    version('2.17.2',   sha256='2e929970d45902b8e4d31eac58d8476bd8eda5dba808033bfd1b3b764481287c')

    depends_on('py-setuptools',         type='build')
    depends_on('py-numpy',              type=('build', 'run'))
