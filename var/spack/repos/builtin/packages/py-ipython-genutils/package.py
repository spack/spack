# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpythonGenutils(PythonPackage):
    """Vestigial utilities from IPython"""

    pypi = "ipython_genutils/ipython_genutils-0.1.0.tar.gz"

    version(
        "0.2.0",
        sha256="72dd37233799e619666c9f639a9da83c34013a73e8bbc79a7a6348d93c61fab8",
        url="https://pypi.org/packages/fa/bc/9bd3b5c2b4774d5f33b2d544f1460be9df7df2fe42f352135381c347c69a/ipython_genutils-0.2.0-py2.py3-none-any.whl",
    )
    version(
        "0.1.0",
        sha256="6218e9abd612fb5acfb175ea7c7b026006de4df9691d9a73c9b390cfa1a41c2b",
        url="https://pypi.org/packages/6a/b3/4ce580020d6be73770d55515a65aec9ed5f3ea95f09e00300e53fc264218/ipython_genutils-0.1.0-py2.py3-none-any.whl",
    )
