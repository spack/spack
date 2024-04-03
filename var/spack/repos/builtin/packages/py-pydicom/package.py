# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydicom(PythonPackage):
    """Pure python package for DICOM medical file reading and writing

    pydicom is a pure Python package for working with DICOM files. It lets you
    read, modify and write DICOM data in an easy "pythonic" way."""

    homepage = "https://github.com/pydicom/pydicom"
    pypi = "pydicom/pydicom-2.1.2.tar.gz"

    version(
        "2.4.3",
        sha256="797e84f7b22e5f8bce403da505935b0787dca33550891f06495d14b3f6c70504",
        url="https://pypi.org/packages/24/fe/d74445ca70ca30328a0c07ba50d9558741882a524ae92a7b482cce7ec6bf/pydicom-2.4.3-py3-none-any.whl",
    )
    version(
        "2.4.1",
        sha256="301cbf8bf2cca95643ccf678f5b0cfecfd15974cd27e199f0856c44694852c0e",
        url="https://pypi.org/packages/76/ce/a941758893f96197d5c96c1f733883a6917d377d3e136a5b65c73a64b03d/pydicom-2.4.1-py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="8ff31e077cc51d19ac3b8ca988ac486099cdebfaf885989079fdc7c75068cdd8",
        url="https://pypi.org/packages/5f/45/97660cc1ec770e2e82fd5d704c1d6ff9c308ecfcbbf07c2b2f92ca755b70/pydicom-2.3.0-py3-none-any.whl",
    )
    version(
        "2.1.2",
        sha256="d97f53a7b269dbd7414d18342f1b70f80d7d35dc4e479316bab146daac0e0c15",
        url="https://pypi.org/packages/f4/15/df16546bc59bfca390cf072d473fb2c8acd4231636f64356593a63137e55/pydicom-2.1.2-py3-none-any.whl",
    )

    variant("numpy", default=False, description="Use NumPy for Pixel data")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.4:")

    # Historical dependencies
