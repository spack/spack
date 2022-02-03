# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytesseract(PythonPackage):
    """Python-tesseract is an Optical Charachter Recognition (OCR) Tool for python."""

    homepage = "https://github.com/madmaze/pytesseract"
    pypi     = "pytesseract/pytesseract-0.3.8.tar.gz"

    version('0.3.8', sha256='6148a01e4375760862e8f56ea718e22b5d13b281454df46ea8dac9807793fc5a')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-packaging@21.3:', type=('build', 'run'))
    depends_on('py-pillow@8.0.0:', type=('build', 'run'))
    # depends_on('py-pip@X.Y:', type='build')
    depends_on('py-wheel@0.29.0:', type='build')

    depends_on('py-setuptools@40.0.4', type='build')
    # depends_on('py-flit-core', type='build')
    # depends_on('py-poetry-core', type='build')

    # depends_on('py-foo', type=('build', 'run'))

