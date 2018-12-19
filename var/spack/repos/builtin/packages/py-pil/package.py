# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPil(PythonPackage):
    """The Python Imaging Library (PIL) adds image processing capabilities
    to your Python interpreter. This library supports many file formats,
    and provides powerful image processing and graphics capabilities."""

    homepage = "http://www.pythonware.com/products/pil/"
    url      = "http://effbot.org/media/downloads/Imaging-1.1.7.tar.gz"

    version('1.1.7', 'fc14a54e1ce02a0225be8854bfba478e')

    provides('pil')

    # py-pil currently only works with Python2.
    # If you are using Python 3, try using py-pillow instead.
    depends_on('python@1.5.2:2.8')
