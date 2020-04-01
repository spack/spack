# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKerasPreprocessing(PythonPackage):
    """Utilities for working with image data, text data, and sequence data."""

    homepage = "http://keras.io"
    url      = "https://github.com/keras-team/keras-preprocessing/archive/1.0.5.tar.gz"

    version('1.1.0', sha256='26f26354370f4a08a029137630d72870e99e924cd8f6e04c2f6fc0bd86708275')
    version('1.0.9', sha256='045a9b3faf4f6d63493cc3ca396659cc0395727b280c988fb9b6c7ff8157f09b')
    version('1.0.5', sha256='8a1d20d8dd2204d82616648f1b40615ea9f5ff0f8f94fdc6d9fe3c2238476c89')
    version('1.0.4', sha256='9f36ffeab4545f039880d6eaf8f8b3a6c8eba14618cec25c60d69a281398e5ea')
    version('1.0.3', sha256='7a7da86eaae0cadfd83e644741898d1edbd6819631ff0ee36fd130bd9efd814e')
    version('1.0.2', sha256='64212b715a435b43724ecf26be67a441cee426e3ef614a6326aba06016ba9779')
    version('1.0.1', sha256='2e9e187afd1327d802309513cc6366d72a5c02104c6815da30d8651a4bd20699')

    depends_on('py-setuptools', type='build')
