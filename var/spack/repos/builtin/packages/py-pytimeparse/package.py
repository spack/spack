# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytimeparse(PythonPackage):
    """A small Python library to parse various kinds of time expressions."""

    homepage = "https://github.com/wroberts/pytimeparse"
    pypi = "pytimeparse/pytimeparse-1.1.8.tar.gz"

    license("MIT")

    version(
        "1.1.8",
        sha256="04b7be6cc8bd9f5647a6325444926c3ac34ee6bc7e69da4367ba282f076036bd",
        url="https://pypi.org/packages/1b/b4/afd75551a3b910abd1d922dbd45e49e5deeb4d47dc50209ce489ba9844dd/pytimeparse-1.1.8-py2.py3-none-any.whl",
    )
