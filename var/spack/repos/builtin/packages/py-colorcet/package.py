# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyColorcet(PythonPackage):
    """A collection of perceptually acccurate 256-color colormaps for use with
    Python plotting programs like Bokeh, Matplotlib, HoloViews, and Datashader."""

    homepage = "https://colorcet.holoviz.org/index.html"
    pypi = "colorcet/colorcet-3.0.0.tar.gz"

    maintainers("vvolkl")

    version(
        "3.0.0",
        sha256="074027a442921813d4328f03c200a55c8ac73d19901919abcd0c6fb67fa79664",
        url="https://pypi.org/packages/fc/db/d55e0d28e01d3f24cb5bcb8023437fc5fa2371f42e578a65251344690610/colorcet-3.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-param@1.7:", when="@:3.0.0-alpha7,3.0.0")
        depends_on("py-pyct@0.4.4:", when="@:3.0")
