# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMatplotlibScalebar(PythonPackage):
    """Provides a new artist for matplotlib to display a scale bar,
    aka micron bar."""

    homepage = "https://github.com/ppinard/matplotlib-scalebar"
    pypi = "matplotlib-scalebar/matplotlib-scalebar-0.6.1.tar.gz"
    git = "https://github.com/ppinard/matplotlib-scalebar.git"

    license("BSD-2-Clause")

    version(
        "0.8.1",
        sha256="a8a2f361d4c2d576d087df3092ed95cac2f708f8b40d5d2bb992bd190e740b3a",
        url="https://pypi.org/packages/a9/9e/22930e3deb2c374f47c6633aff9f6f379f8c421ab868fff3b4f85eac8b8a/matplotlib_scalebar-0.8.1-py2.py3-none-any.whl",
    )
    version(
        "0.6.1",
        sha256="913e0c2e3f7039d6e3d3f8bfb569241b3baaa747bfc1ec842ceec1adc1c2013f",
        url="https://pypi.org/packages/d1/95/d311da1083a426b872e7be318373c45f075bb356d0524c3097f5f4c6d2d9/matplotlib_scalebar-0.6.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@0.8:")
        depends_on("py-matplotlib", when="@0.3:")
