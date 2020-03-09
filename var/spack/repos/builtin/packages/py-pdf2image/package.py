# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPdf2image(PythonPackage):
    """A python module that wraps the pdftoppm utility to convert PDF to
    PIL Image object"""

    homepage = "https://pypi.org/project/pdf2image/"
    url      = "https://pypi.io/packages/source/p/pdf2image/pdf2image-1.12.1.tar.gz"

    version('1.12.1', sha256='a0d9906f5507192210a8d5d7ead63145e9dec4bccc4564b1fb644e923913c31c')

    depends_on('py-setuptools', type='build')

    depends_on('py-pillow', type='run')
    depends_on('poppler', type='run')
