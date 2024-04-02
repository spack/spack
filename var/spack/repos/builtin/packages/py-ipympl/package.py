# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpympl(PythonPackage):
    """Matplotlib Jupyter Extension."""

    homepage = "https://github.com/matplotlib/ipympl"
    pypi = "ipympl/ipympl-0.8.8.tar.gz"
    maintainers("haralmha")

    license("BSD-3-Clause")

    version(
        "0.8.8",
        sha256="86468aeaae8c0a28007d0c7f6dbb85f2b6cb9805167e88d4daa7529562009159",
        url="https://pypi.org/packages/81/13/12a4761eb01a59e7f185af7b9543a9aef9495c42a5f77d8b8c4d51794f8c/ipympl-0.8.8-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-ipython", when="@0.8.6:")
        depends_on("py-ipython-genutils", when="@0.8.5:")
        depends_on("py-ipywidgets@7.6.0:7", when="@0.8.5:0.9.1")
        depends_on("py-matplotlib@2.0.0:", when="@0.8.5:0.8")
        depends_on("py-numpy", when="@0.8.5:")
        depends_on("py-pillow", when="@0.8.5:")
        depends_on("py-traitlets", when="@0.8.5:")
