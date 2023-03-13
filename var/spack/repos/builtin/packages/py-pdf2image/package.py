# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPdf2image(PythonPackage):
    """A python module that wraps the pdftoppm utility to convert PDF to PIL Image object"""

    homepage = "https://pypi.org/project/pdf2image/"
    pypi = "pdf2image/pdf2image-1.12.1.tar.gz"

    version("1.16.2", sha256="86761091eee35f4641ea98dfddb254254361d018be698a199aff7c1d37331803")
    version("1.12.1", sha256="a0d9906f5507192210a8d5d7ead63145e9dec4bccc4564b1fb644e923913c31c")

    depends_on("py-setuptools", type="build")

    depends_on("py-pillow", type=("build", "run"))
    depends_on("poppler", type=("build", "run"))
