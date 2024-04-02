# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCatalogue(PythonPackage):
    """catalogue: Super lightweight function registries for your library."""

    homepage = "https://github.com/explosion/catalogue"
    pypi = "catalogue/catalogue-2.0.0.tar.gz"

    license("MIT")

    version(
        "2.0.8",
        sha256="2d786e229d8d202b4f8a2a059858e45a2331201d831e39746732daa704b99f69",
        url="https://pypi.org/packages/dc/28/a2b0cc4bfa7916ef9caf08475be5810fc564411c5a801f225a1f40a458c5/catalogue-2.0.8-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="218103923efff9120e4082712015464ef2a594bca18e0a2111c8c038332da502",
        url="https://pypi.org/packages/e3/8e/9391f722c58dc202cb7980a3a1f0e2499cc91e1fbda2c17632dad1b6e299/catalogue-2.0.0-py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="584d78e7f4c3c6e2fd498eb56dfc8ef1f4ff738480237de2ccd26cbe2cf47172",
        url="https://pypi.org/packages/6c/f9/9a5658e2f56932e41eb264941f9a2cb7f3ce41a80cb36b2af6ab78e2f8af/catalogue-1.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-typing-extensions@3.6.5:", when="@1.0.1:1,2.0.3: ^python@:3.7")
        depends_on("py-zipp@0.5:", when="@1.0.1:1,2.0.3: ^python@:3.7")
