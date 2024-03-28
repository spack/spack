# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPlac(PythonPackage):
    """The smartest command line arguments parser in the world."""

    homepage = "https://github.com/micheles/plac"
    pypi = "plac/plac-1.1.3.tar.gz"

    # Skip 'plac_tk' imports
    import_modules = ["plac", "plac_ext", "plac_core"]

    license("BSD-2-Clause")

    version(
        "1.3.5",
        sha256="a8933d21a40fe2cec177a2f96217425a4e889d275aa3e25ecf9a9640ab16d416",
        url="https://pypi.org/packages/cb/3b/7b0c4f0afb9d33dd901bab5714b2303e880f3d76ac3a12fe3b48a12dbc78/plac-1.3.5-py2.py3-none-any.whl",
    )
    version(
        "1.3.3",
        sha256="88d8f064f1bbf20dd474ca8e8b4d6c9135684a889b7bbf3d7399ad17c2589cbe",
        url="https://pypi.org/packages/a3/ec/9ca538f3dc96df2410be120fc9833f41656f358c0b2297797c91fe433db8/plac-1.3.3-py2.py3-none-any.whl",
    )
    version(
        "1.1.3",
        sha256="487e553017d419f35add346c4c09707e52fa53f7e7181ce1098ca27620e9ceee",
        url="https://pypi.org/packages/86/85/40b8f66c2dd8f4fd9f09d59b22720cffecf1331e788b8a0cab5bafb353d1/plac-1.1.3-py2.py3-none-any.whl",
    )
