# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAffine(PythonPackage):
    """Matrices describing affine transformation of the plane."""

    homepage = "https://github.com/sgillies/affine"
    url = "https://github.com/sgillies/affine/archive/2.1.0.zip"

    version(
        "2.1.0",
        sha256="ed8bc4b217ec051c07c2733bc60229a0dfd00d88bbe0b94db992e65a0d876bc4",
        url="https://pypi.org/packages/c9/24/71214ac2b93db5b64775821ed32dd6f9da451d51dbb83cb0b66fa38acac7/affine-2.1.0-py3-none-any.whl",
    )

    license("BSD-3-Clause")
