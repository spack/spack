# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDistlib(PythonPackage):
    """Distribution utilities"""

    homepage = "https://bitbucket.org/pypa/distlib"
    pypi = "distlib/distlib-0.3.6.tar.gz"

    license("PSF-2.0")

    version(
        "0.3.7",
        sha256="2e24928bc811348f0feb63014e97aaae3037f2cf48712d51ae61df7fd6075057",
        url="https://pypi.org/packages/43/a0/9ba967fdbd55293bacfc1507f58e316f740a3b231fc00e3d86dc39bc185a/distlib-0.3.7-py2.py3-none-any.whl",
    )
    version(
        "0.3.6",
        sha256="f35c4b692542ca110de7ef0bea44d73981caeb34ca0b9b6b2e6d7790dda8f80e",
        url="https://pypi.org/packages/76/cb/6bbd2b10170ed991cf64e8c8b85e01f2fb38f95d1bc77617569e0b0b26ac/distlib-0.3.6-py2.py3-none-any.whl",
    )
    version(
        "0.3.4",
        sha256="6564fe0a8f51e734df6333d08b8b94d4ea8ee6b99b5ed50613f731fd4089f34b",
        url="https://pypi.org/packages/ac/a3/8ee4f54d5f12e16eeeda6b7df3dfdbda24e6cc572c86ff959a4ce110391b/distlib-0.3.4-py2.py3-none-any.whl",
    )
    version(
        "0.3.3",
        sha256="c8b54e8454e5bf6237cc84c20e8264c3e991e824ef27e8f1e81049867d861e31",
        url="https://pypi.org/packages/28/36/4bdfb663826d6deedc30b179a7b7876a86943cec9fcfc3f1638489fd8b09/distlib-0.3.3-py2.py3-none-any.whl",
    )

    # pip silently replaces distutils with setuptools
