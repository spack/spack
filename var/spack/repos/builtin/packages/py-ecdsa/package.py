# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEcdsa(PythonPackage):
    """ECDSA cryptographic signature library (pure python)"""

    homepage = "https://github.com/warner/python-ecdsa"
    pypi = "ecdsa/ecdsa-0.15.tar.gz"

    license("MIT")

    version(
        "0.15",
        sha256="867ec9cf6df0b03addc8ef66b56359643cb5d0c1dc329df76ba7ecfe256c8061",
        url="https://pypi.org/packages/b8/11/4b4d30e4746584684c758d8f1ddc1fa5ab1470b6bf70bce4d9b235965e99/ecdsa-0.15-py2.py3-none-any.whl",
    )
    version(
        "0.13.2",
        sha256="20c17e527e75acad8f402290e158a6ac178b91b881f941fc6ea305bfdfb9657c",
        url="https://pypi.org/packages/23/a8/8aa68e70959e1287da9154e5164bb8bd5dd7025e41ae54e8d177b8d165c9/ecdsa-0.13.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six@1.9:", when="@0.15:")
